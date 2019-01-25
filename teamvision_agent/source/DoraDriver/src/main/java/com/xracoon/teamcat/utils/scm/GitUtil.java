package com.xracoon.teamcat.utils.scm;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.List;
import org.eclipse.jgit.api.CheckoutCommand;
import org.eclipse.jgit.api.CheckoutCommand.Stage;
import org.eclipse.jgit.api.CloneCommand;
import org.eclipse.jgit.api.CreateBranchCommand.SetupUpstreamMode;
import org.eclipse.jgit.api.FetchCommand;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.LogCommand;
import org.eclipse.jgit.api.ResetCommand;
import org.eclipse.jgit.api.ResetCommand.ResetType;
import org.eclipse.jgit.api.errors.CheckoutConflictException;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.api.errors.InvalidRefNameException;
import org.eclipse.jgit.api.errors.NoHeadException;
import org.eclipse.jgit.api.errors.RefAlreadyExistsException;
import org.eclipse.jgit.api.errors.RefNotFoundException;
import org.eclipse.jgit.diff.DiffEntry;
import org.eclipse.jgit.diff.RenameDetector;
import org.eclipse.jgit.errors.CorruptObjectException;
import org.eclipse.jgit.errors.IncorrectObjectTypeException;
import org.eclipse.jgit.errors.MissingObjectException;
import org.eclipse.jgit.errors.NoWorkTreeException;
import org.eclipse.jgit.lib.ObjectReader;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.transport.UsernamePasswordCredentialsProvider;
import org.eclipse.jgit.treewalk.TreeWalk;
import org.eclipse.jgit.treewalk.filter.TreeFilter;
import org.slf4j.LoggerFactory;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;

//https://github.com/jenkinsci/git-client-plugin/blob/835441a1616f323687c151db58c62cac996655a9/src/main/java/org/jenkinsci/plugins/gitclient/JGitAPIImpl.java

/**
 * Deprecated due to performance issues
 * @author Administrator
 */
@Deprecated 
public class GitUtil extends ScmUtil{
	
	public GitUtil(String url, String branchOrVersion, String path,
			String userName, char[] password, int strategy) {
		super(url, StringEx.isBlank(branchOrVersion)?"master":branchOrVersion, path, userName, password, strategy);
		logger = LoggerFactory.getLogger(GitUtil.class);
	}
	
	//从已有的目录中创建
	public GitUtil(String path){
		
	}
	
	@Override
	public boolean exec() throws Exception {
		if(strategy==ScmUtil.GIT_STRATEGY_SHALLOW_CLONE){
			logger.info("shallow clone...");
			return checkout();
		}
		else if(strategy==ScmUtil.GIT_STRATEGY_FULL_CLONE){
			logger.info("full clone...");
			return checkout();
		}
		else if(strategy==ScmUtil.GIT_STRATEGY_UPDATE){
			logger.info("update new commits...");
			return update();
		}
		else{
			logger.error("unknown git strategy "+strategy);
			return false;
		}
	}
	
	//clone
	@Override
	public boolean checkout() throws NoWorkTreeException, IOException, GitAPIException {
		if(path.exists() && !FilesEx.deleteTree(path)){
			logger.error("can not wipe out source path");
			return false;
		}
		
		//clone
		logger.info("Clone to repository:");
		CloneCommand cloneCmd = new CloneCommand();
		cloneCmd.setTimeout(15*60*1000); //15min
		cloneCmd.setCloneAllBranches(true);
		cloneCmd.setDirectory(path);
		cloneCmd.setURI(repository);
		cloneCmd.setCredentialsProvider(new UsernamePasswordCredentialsProvider(this.userName, new String(this.password)));
		cloneCmd.setBranch(this.branchOrVersion); //the initial branch to check out
		cloneCmd.setNoCheckout(true);
		
		
		Git git=null;
		try {
			git=cloneCmd.call();
			checkoutCommit(git, this.branchOrVersion);
			return true;
		} catch (GitAPIException e) {
			throw e;
		}
		finally{
			if(git!=null)
				git.close();
		}
		
//		if(!(branchOrVersion.equals("")||branchOrVersion.isEmpty()))
//			checkOutBranch(path, branchOrVersion);//改成localPath,去掉projectName
	}
	
	private void checkoutCommit(Git git, String branchOrVersion) throws RefAlreadyExistsException, RefNotFoundException, InvalidRefNameException, CheckoutConflictException, GitAPIException{
		CheckoutCommand coCmd = git.checkout();
		coCmd.setForce(true);
		coCmd.setName(this.branchOrVersion);
		coCmd.setStage(Stage.THEIRS);
		coCmd.setUpstreamMode(SetupUpstreamMode.SET_UPSTREAM);
		coCmd.call();
	}
	
	@Override
	public boolean update() {
		Git git=null;
		try{
			if(!new File(this.path,".git").exists()){
				this.strategy=ScmUtil.GIT_STRATEGY_FULL_CLONE;
				return checkout();
			}
			
			git=Git.open(path);
			
			//reset
			ResetCommand resetCmd = new ResetCommand(git.getRepository());
			resetCmd.setMode(ResetType.HARD);
			resetCmd.call();
			
			//fetch
			FetchCommand fetchCmd = git.fetch();
			fetchCmd.setCredentialsProvider(new UsernamePasswordCredentialsProvider(this.userName, new String(this.password)));
			fetchCmd.setRemoveDeletedRefs(true);
			fetchCmd.call();
			
			//chekcout
			checkoutCommit(git, this.branchOrVersion);
			
			return true;
			
		} catch (IOException | GitAPIException e) {
			logger.error("exception occur when update", e);
			return false;
		}
		finally{
			if(git!=null)
				git.close();
		}
	}	
	
	public ArrayList<String> getAllVersion(File path) throws IOException, NoHeadException, GitAPIException
	{
		Git git=null;
		try {
			git = Git.open(path);
			LogCommand logCommand = git.log();
			Iterable<RevCommit> logIterable = logCommand.call();
			Iterator<RevCommit> logIterator = logIterable.iterator();
			ArrayList<String> objectId = new ArrayList<String>();
			while(logIterator.hasNext()) {
				RevCommit rev = logIterator.next();			
				objectId.add(rev.getId().getName());
			} 
			return objectId;
		}catch (Exception e) {
			logger.error(e.getMessage(), e);
			return null;
		}
		finally{
			git.close();
		}
	}

	private List<Change> getRevChanges(Repository repo, RevCommit commit, RevCommit parent) throws MissingObjectException, IncorrectObjectTypeException, CorruptObjectException, IOException{
		ObjectReader objReader = repo.newObjectReader();
		TreeWalk tw = new TreeWalk(objReader);
		if(parent!=null)
			tw.reset(parent.getTree(), commit.getTree());
		else {
			if(commit.getParentCount()>0)
				tw.reset(commit.getParent(0).getTree(), commit.getTree());
			else
				tw.reset(commit.getTree(), commit.getTree());
		}
		tw.setRecursive(true);
        tw.setFilter(TreeFilter.ANY_DIFF);
        final RenameDetector rd = new RenameDetector(repo);
        rd.reset();
        rd.addAll(DiffEntry.scan(tw));
        List<DiffEntry> diffs = rd.compute(objReader, null);
        List<Change> changes=new ArrayList<>();
        for(DiffEntry diff: diffs){
        	Change change=new Change();
        	change.setType(Change.ChangeType.valueOf(diff.getChangeType().toString().substring(0, 1)));
        	change.setNewPath(diff.getNewPath());
        	change.setOldPath(diff.getOldPath());
        	changes.add(change);
        }
        
		return changes;
	}
	
	@Override
	public List<Revision> getChangeSet(String untilToVersion) {
		List<Revision> list=new ArrayList<>();
		if(StringEx.isBlank(untilToVersion))
			return list;
		
		boolean find=false;
		Git git=null;
		SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		try {
			git = Git.open(path);
			LogCommand logCmd = git.log();
			logCmd.setMaxCount(100);//最多输出
			Iterable<RevCommit> logIterable = logCmd.call();
			Iterator<RevCommit> logIterator = logIterable.iterator();
			
			//RevWalk
			//new ... old
			while(logIterator.hasNext()) {
				RevCommit rev = logIterator.next();
				if(rev.getId().getName().startsWith(untilToVersion.toLowerCase())){
					//list.add(new Revision(rev.getId().name(), rev.getAuthorIdent().getName(), sdf.format(new Date((long)rev.getCommitTime()*1000)), rev.getFullMessage()));
					find=true;
					break;
				}
				List<Change> changes=getRevChanges(git.getRepository(), rev, null);
				list.add(new Revision(rev.getId().name(), rev.getAuthorIdent().getName(),rev.getAuthorIdent().getEmailAddress(), sdf.format(new Date((long)rev.getCommitTime()*1000)), rev.getFullMessage(), changes));
			} 
		}catch (Exception e) {
			git.close();
			logger.error(e.getMessage(), e);
		}
		finally{
			if(git!=null)
				git.close();
		}
		return find?list:new ArrayList<Revision>();
	}

	@Override
	public String getVersion() {
		Git git=null;
		try {
			git = Git.open(path);
			LogCommand logCommand = git.log();
			Iterable<RevCommit> logIterable = logCommand.call();
			Iterator<RevCommit> logIterator = logIterable.iterator();
			RevCommit commit = logIterator.next();
			return commit.getId().getName();
		}catch (Exception e) {
			logger.error(e.getMessage(), e);
			return null;
		}
		finally{
			if(git!=null)
				git.close();
		}
	}
}
