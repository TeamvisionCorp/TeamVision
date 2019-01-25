package com.xracoon.teamcat.utils.scm;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Iterator;
import java.util.List;
import org.eclipse.jgit.api.Git;
import org.eclipse.jgit.api.LogCommand;
import org.eclipse.jgit.api.errors.GitAPIException;
import org.eclipse.jgit.api.errors.NoHeadException;
import org.eclipse.jgit.diff.DiffEntry;
import org.eclipse.jgit.diff.RenameDetector;
import org.eclipse.jgit.errors.CorruptObjectException;
import org.eclipse.jgit.errors.IncorrectObjectTypeException;
import org.eclipse.jgit.errors.MissingObjectException;
import org.eclipse.jgit.lib.ObjectReader;
import org.eclipse.jgit.lib.Repository;
import org.eclipse.jgit.revwalk.RevCommit;
import org.eclipse.jgit.treewalk.TreeWalk;
import org.eclipse.jgit.treewalk.filter.TreeFilter;
import org.slf4j.LoggerFactory;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.RandomEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

//https://github.com/jenkinsci/git-client-plugin/blob/835441a1616f323687c151db58c62cac996655a9/src/main/java/org/jenkinsci/plugins/gitclient/JGitAPIImpl.java

public class CmdGitUtil extends ScmUtil{
	
	public CmdGitUtil(String url, String branchOrVersion, String path,
			String userName, char[] password, int strategy) {
		super(url, StringEx.isBlank(branchOrVersion)?"master":branchOrVersion, path, userName, password, strategy);
		logger = LoggerFactory.getLogger(CmdGitUtil.class);
	}
	
	//从已有的目录中创建
	public CmdGitUtil(String path){
		
	}
	
	private String mergeCred() throws UnsupportedEncodingException{
		if(repository.contains("@") && repository.contains(":"))
			return repository;
		
		int idx=repository.indexOf("://");
		idx= idx==-1?0:idx+3;
		repository=repository.substring(0,idx)
				+ URLEncoder.encode(this.userName,"UTF-8")+":"
				+ URLEncoder.encode(new String(this.password).trim(),"UTF-8")
				+ "@"+repository.substring(idx);
		return repository;
	}
	
	private File credTempFile;
	private long credLength;
	private void writeCred() throws IOException{
		credTempFile= new File(path,".git/objects/info/.cre");//Files.createTempFile("","").toFile().getCanonicalFile();
		String mergeUrl=mergeCred();
		int idxOfAt=mergeUrl.indexOf("@");
		String credLine=mergeUrl.substring(0, mergeUrl.indexOf("/", idxOfAt));
		credLength=credLine.length();
		FilesEx.writeFile(credLine, credTempFile);
		
		OS os=OS.getSingleton();
		os.execSyn(new String[]{"git", "config","--local","credential.username", this.userName}, null, path, false);
		os.execSyn(new String[]{"git", "config","--local","credential.helper", "store --file "+credTempFile.getCanonicalPath().replace("\\", "/")}, null, path, false);
	}
	
	private void cleanCred() throws IOException{
		OS.getSingleton().execSyn(new String[]{"git","config","--local","--remove-section", "credential"}, null, path, false);
		if(credTempFile!=null && credTempFile.exists()){
			//cover old data
			FilesEx.writeFile(RandomEx.randomString(credLength), credTempFile);
			FilesEx.writeFile(RandomEx.randomString(credLength), credTempFile);
			credTempFile.delete();
			credTempFile=null;
			credLength=0;
		}
	}
	
	//clone
	@Override
	public boolean checkout() throws Exception {
		if(path.exists() && !FilesEx.deleteContent(path)){
			logger.error("can not wipe out source path");
			return false;
		}
		path.mkdirs();
		
		OS os=OS.getSingleton();
		try{
			List<String> cmds=new ArrayList<>(Arrays.asList(new String[]{"git", "fetch", "--progress", "-v", "-f", 
					this.repository, "+refs/heads/*:refs/remotes/origin/*"}));
			
			if(this.strategy==GIT_STRATEGY_SHALLOW_CLONE)
				cmds.addAll(2, Arrays.asList(new String[]{"--depth", "1"}));
			
			os.execSyn("git init",null, path);
			//os.execSyn("git remote add origin "+this.repository, null, path);
			writeCred();
			ExecStatus es= os.execSyn(cmds.toArray(new String[0]), null, path); //fetch
			if(es.getRetVal()!=0)
				throw new Exception("git fetch failed!");
			
			String branch="";
			if(this.branchOrVersion.contains("/"))
			{
				branch=this.branchOrVersion;
			}
			else if(this.branchOrVersion.toUpperCase().startsWith("TAG:"))
			{
				branch=this.branchOrVersion.replaceFirst("tag:","").replaceFirst("TAG:","");
			}
			else
			{
				branch="origin/"+this.branchOrVersion;
			}
			
			es= os.execSyn("git checkout "+branch, null, path);
			if(es.getRetVal()!=0)
				throw new Exception("git checkout failed!");
			return es.getRetVal()==0;
		}finally{
			cleanCred();
		}
	}
	
	@Override
	public boolean update() throws Exception {
		OS os=OS.getSingleton();
		try{
			//本地repo无效， 转为full clone
			ExecStatus es=OS.getSingleton().execSyn("git reset --hard", null, path);
			if(es.getRetVal()!=0){
				logger.warn("invailed local repo or reset failed, using 'full clone' strategy! ");
				this.strategy=ScmUtil.GIT_STRATEGY_FULL_CLONE;
				return checkout();
			}
			es=OS.getSingleton().execSyn("git clean -xfd", null, path);
			if(es.getRetVal()!=0){
				logger.warn("invailed local repo or clean failed, using 'full clone' strategy! ");
				this.strategy=ScmUtil.GIT_STRATEGY_FULL_CLONE;
				return checkout();
			}
			
			List<String> cmds=new ArrayList<>(Arrays.asList(new String[]{"git", "fetch", "--progress", "-v", "-f", 
					this.repository, "+refs/heads/*:refs/remotes/origin/*"}));
			writeCred();
			es=os.execSyn(cmds.toArray(new String[0]), null, path); //fetch
			if(es.getRetVal()!=0)
				throw new Exception("git fetch failed!");
			es= os.execSyn("git checkout "+(this.branchOrVersion.contains("/")?branchOrVersion:"origin/"+branchOrVersion), null, path);
			if(es.getRetVal()!=0)
				throw new Exception("git checkout failed!");
			return es.getRetVal()==0;
		}finally{
			cleanCred();
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
}
