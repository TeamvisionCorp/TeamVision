package com.xracoon.teamcat.utils.scm;

import java.io.File;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.tmatesoft.svn.core.ISVNLogEntryHandler;
import org.tmatesoft.svn.core.SVNDepth;
import org.tmatesoft.svn.core.SVNException;
import org.tmatesoft.svn.core.SVNLogEntry;
import org.tmatesoft.svn.core.SVNLogEntryPath;
import org.tmatesoft.svn.core.SVNURL;
import org.tmatesoft.svn.core.internal.io.dav.DAVRepositoryFactory;
import org.tmatesoft.svn.core.internal.io.fs.FSRepositoryFactory;
import org.tmatesoft.svn.core.internal.io.svn.SVNRepositoryFactoryImpl;
import org.tmatesoft.svn.core.internal.wc.DefaultSVNOptions;
import org.tmatesoft.svn.core.wc.ISVNExternalsHandler;
import org.tmatesoft.svn.core.wc.SVNClientManager;
import org.tmatesoft.svn.core.wc.SVNEvent;
import org.tmatesoft.svn.core.wc.SVNEventAction;
import org.tmatesoft.svn.core.wc.SVNEventAdapter;
import org.tmatesoft.svn.core.wc.SVNRevision;
import org.tmatesoft.svn.core.wc.SVNStatus;
import org.tmatesoft.svn.core.wc.SVNStatusType;
import org.tmatesoft.svn.core.wc.SVNUpdateClient;
import org.tmatesoft.svn.core.wc.SVNWCUtil;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;

public class SvnUtil extends ScmUtil{
	private SVNURL svnRepo;
	private SVNRevision svnRevision;
	
	public SvnUtil(String url, String branchOrVersion, String localPath,
			String userName, char[] password, int strategy) throws SVNException {
		super(url, StringEx.isBlank(branchOrVersion)?"master":branchOrVersion, localPath, userName, password, strategy);
		logger = LoggerFactory.getLogger(SvnUtil.class);
		svnRepo = SVNURL.parseURIEncoded(url);
		svnRevision= StringEx.isBlank(branchOrVersion)?SVNRevision.HEAD:SVNRevision.parse(branchOrVersion);
		setupLibrary(svnRepo.getProtocol());
	}
	
	public SvnUtil(String path){
		
	}
	
	@Override
	public boolean exec() throws Exception {
		if(strategy==ScmUtil.SVN_STRATEGY_CHECKOUT){
			logger.info("fresh checkout");
			return checkout();
		}
		else if(strategy==ScmUtil.SVN_STRATEGY_UPDATE){
			logger.info("update");
			return update();
		}
		else{
			logger.error("unknown svn strategy "+strategy);
			return false;
		}
	}
	
	@Override
	public boolean checkout() throws Exception {
		if(path.exists() && !FilesEx.deleteTree(path))
			throw new Exception("failed to clean workcopy");
		
		logger.info("Checkout start...");
		DefaultSVNOptions options = SVNWCUtil.createDefaultOptions(true);
		options.setAuthStorageEnabled(keepCredential);
		SVNClientManager clientManager = SVNClientManager.newInstance(options, userName, new String(password));
		try{
			SVNUpdateClient updateClient = clientManager.getUpdateClient();
			EventHandlerImpl eventHandler = new EventHandlerImpl();
			updateClient.setEventHandler(eventHandler);
            updateClient.setExternalsHandler(eventHandler);
             
			updateClient.setIgnoreExternals(false);
			updateClient.doCheckout(svnRepo, path, svnRevision, svnRevision, SVNDepth.INFINITY, false);
			
			logger.info("Checkout finished!");
		}
		catch(Exception e){
			throw e;
		}
		finally{
			if(clientManager!=null)
				clientManager.dispose();
		}
		return true;
	}

	@Override
	public boolean update() throws Exception  {
		//检查状态，非svn工作区则checkout
		SVNStatus status=null;
		DefaultSVNOptions options = SVNWCUtil.createDefaultOptions(true);
		options.setAuthStorageEnabled(keepCredential);
		SVNClientManager clientManager = SVNClientManager.newInstance(options, userName, new String(password));
		try{
			try {	
				status=clientManager.getStatusClient().doStatus(path, true);
				if(!status.getURL().toString().equals(this.repository)){
					logger.warn("existing workcopy not match new url, use 'checkout' strategy!");
					return checkout();
				}
				
				//reset
				logger.info("revert...");
				clientManager.getWCClient().doRevert(new File[]{path}, SVNDepth.INFINITY, null);
			} catch (SVNException e) {
				logger.warn("existing workcopy check failed, use 'checkout' strategy!");
				return checkout();
			}
			
			//检查版本，有更新则update
			SVNRevision revision=StringEx.isBlank(branchOrVersion)?SVNRevision.HEAD:SVNRevision.parse(branchOrVersion);
			if(status.getRemoteRevision().getNumber()!=revision.getNumber()){
				logger.info("Update Start...");
				SVNUpdateClient updateClient = clientManager.getUpdateClient(); 
				EventHandlerImpl eventHandler = new EventHandlerImpl();
				updateClient.setEventHandler(eventHandler);
	            updateClient.setExternalsHandler(eventHandler);
	            
	        	updateClient.setIgnoreExternals(false);   
	        	updateClient.doUpdate(path, revision, SVNDepth.INFINITY, false, false);  
	        	logger.info("Update finished!");
	        }
			else
				logger.info("no change!");
		}catch(Exception e){
			throw e;
		}finally{
			clientManager.dispose();
		}
		return true;
	}
	
	/*
	 * 通过不同协议初始化版本库
	 */
	private void setupLibrary(String protocol){
		if(protocol.contains("http")){
			DAVRepositoryFactory.setup();
		}
		else if(protocol.contains("svn")){
			SVNRepositoryFactoryImpl.setup();
		}
		else if(protocol.contains("file///")){
			FSRepositoryFactory.setup();
		}
		else {
			logger.error("Only support http, https,svn,file protocol!!!");
		}
	}
	
	private List<Change> getRevChange(Map<String, SVNLogEntryPath> changePaths){
		List<Change> changes=new ArrayList<>();
		for(SVNLogEntryPath log: changePaths.values()){
			Change change=new Change();
			change.setType(Change.ChangeType.valueOf(log.getType()+""));
			change.setOldPath(log.getPath());
			change.setNewPath(log.getPath());
			changes.add(change);
		}
		return changes;
	}
	
	@Override
	public List<Revision> getChangeSet(final String untilToVersion){
		final List<Revision> list=new ArrayList<>();
		final SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		DefaultSVNOptions options = SVNWCUtil.createDefaultOptions(true);
		options.setAuthStorageEnabled(keepCredential);
		SVNClientManager clientManager = SVNClientManager.newInstance(options, userName, new String(password));
		SVNRevision curVersion= SVNRevision.parse(getVersion());
		logger.info("get changeset between "+untilToVersion+" and "+ curVersion);
		try {
			clientManager.getLogClient().doLog(new File[]{path}, curVersion, SVNRevision.parse(untilToVersion), curVersion, false, true, true, 0l, null, new ISVNLogEntryHandler(){
				@Override
				public void handleLogEntry(SVNLogEntry logEntry) throws SVNException {
					if(!(logEntry.getRevision()+"").equals(untilToVersion)){
						List<Change> changes=getRevChange(logEntry.getChangedPaths());
						list.add(new Revision(logEntry.getRevision()+"", logEntry.getAuthor(), null ,logEntry.getDate()!=null?sdf.format(logEntry.getDate()):null, logEntry.getMessage(), changes));
					}
				}
			});
		} catch (SVNException e) {
			logger.error("get change set exception", e);
		}
		finally{
			clientManager.dispose();
		}
		return list;
	}

	@Override
	public String getVersion() {
		DefaultSVNOptions options = SVNWCUtil.createDefaultOptions(true);
		options.setAuthStorageEnabled(keepCredential);
		SVNClientManager clientManager = SVNClientManager.newInstance(options, userName, new String(password));
		try {
			return clientManager.getStatusClient().doStatus(path, true).getCommittedRevision().getNumber()+"";
		} catch (SVNException e) {
			logger.error(e.getMessage(), e);
			return null;
		}
		finally{
			clientManager.dispose();
		}
	}
	

	public static class EventHandlerImpl  extends SVNEventAdapter implements ISVNExternalsHandler{
		public Logger logger=LoggerFactory.getLogger(EventHandlerImpl.class);
		private final Map<File, SVNExternalDetails> externalDetails = new HashMap<File, SVNExternalDetails>();
		
		
		public void handleEvent(SVNEvent event, double progress) throws SVNException{
			SVNEventAction action = event.getAction();
	        if (action == SVNEventAction.UPDATE_EXTERNAL) {
	            File file = event.getFile();
	            SVNExternalDetails details = externalDetails.remove(file);
	            logger.info("Fetching external '"+details.getUrl()+"' at "+details.getRevision()+" into "+file);
	        }
	        handleNormal(event, progress);
		}
		
		public void handleNormal(SVNEvent event, double progress) throws SVNException {
	        File path = event.getFile();
	        SVNEventAction action = event.getAction();
	        {// commit notifications
	            if (action == SVNEventAction.COMMIT_ADDED) {
	            	logger.info("Adding         " + path);
	                return;
	            }
	            if (action == SVNEventAction.COMMIT_DELETED) {
	                logger.info("Deleting       " + path);
	                return;
	            }
	            if (action == SVNEventAction.COMMIT_MODIFIED) {
	                logger.info("Sending        " + path);
	                return;
	            }
	            if (action == SVNEventAction.COMMIT_REPLACED) {
	                logger.info("Replacing      " + path);
	                return;
	            }
	            if (action == SVNEventAction.COMMIT_DELTA_SENT) {
	                logger.info("Transmitting file data....");
	                return;
	            }
	        }

	        String pathChangeType = " ";
	        if (action == SVNEventAction.UPDATE_ADD) {
	            pathChangeType = "A";
	            SVNStatusType contentsStatus = event.getContentsStatus();
	            if(contentsStatus== SVNStatusType.UNCHANGED) {
	                // happens a lot with merges
	                pathChangeType = " ";
	            }else if (contentsStatus == SVNStatusType.CONFLICTED) {
	                pathChangeType = "C";
	            } else if (contentsStatus == SVNStatusType.MERGED) {
	                pathChangeType = "G";
	            }
	        } else if (action == SVNEventAction.UPDATE_DELETE) {
	            pathChangeType = "D";
	        } else if (action == SVNEventAction.UPDATE_UPDATE) {
	            SVNStatusType contentsStatus = event.getContentsStatus();
	            if (contentsStatus == SVNStatusType.CHANGED) {
	                /*
	                 * the  item  was  modified in the repository (got  the changes
	                 * from the repository
	                 */
	                pathChangeType = "U";
	            } else if (contentsStatus == SVNStatusType.CONFLICTED) {
	                /*
	                 * The file item is in  a  state  of Conflict. That is, changes
	                 * received from the repository during an update, overlap  with
	                 * local changes the user has in his working copy.
	                 */
	                pathChangeType = "C";
	            } else if (contentsStatus == SVNStatusType.MERGED) {
	                /*
	                 * The file item was merGed (those  changes that came from  the
	                 * repository  did  not  overlap local changes and were  merged
	                 * into the file).
	                 */
	                pathChangeType = "G";
	            }
	        } else if (action == SVNEventAction.UPDATE_COMPLETED) {
	            // finished updating
	            logger.info( "At revision " + event.getRevision()+"\t"+event.getFile());
	            return;
	        } else if (action == SVNEventAction.ADD){
	            logger.info("A     " + path);
	            return;
	        } else if (action == SVNEventAction.DELETE){
	            logger.info("D     " + path);
	            return;
	        } else if (action == SVNEventAction.LOCKED){
	            logger.info("L     " + path);
	            return;
	        } else if (action == SVNEventAction.LOCK_FAILED){
	            logger.info("failed to lock    " + path);
	            return;
	        }

	        /*
	         * Now getting the status of properties of an item. SVNStatusType  also
	         * contains information on the properties state.
	         */
	        SVNStatusType propertiesStatus = event.getPropertiesStatus();
	        String propertiesChangeType = " ";
	        if (propertiesStatus == SVNStatusType.CHANGED) {
	            propertiesChangeType = "U";
	        } else if (propertiesStatus == SVNStatusType.CONFLICTED) {
	            propertiesChangeType = "C";
	        } else if (propertiesStatus == SVNStatusType.MERGED) {
	            propertiesChangeType = "G";
	        }

	        String lockLabel = " ";
	        SVNStatusType lockType = event.getLockStatus();
	        if (lockType == SVNStatusType.LOCK_UNLOCKED) {
	            // The lock is broken by someone.
	            lockLabel = "B";
	        }

	        if(pathChangeType.equals(" ") && propertiesChangeType.equals(" ") && lockLabel.equals(" "))
	            // nothing to display here.
	            return;

	        logger.info(pathChangeType
	                + propertiesChangeType
	                + lockLabel
	                + "       "
	                + path);
	    }
		
		@Override
		public SVNRevision[] handleExternal(File externalPath, SVNURL externalURL, SVNRevision externalRevision,
				SVNRevision externalPegRevision, String externalsDefinition, SVNRevision externalsWorkingRevision) {
	        long revisionNumber = -1;
	        if (SVNRevision.isValidRevisionNumber(externalRevision.getNumber())) {
	            revisionNumber = externalRevision.getNumber();
	        } else if (SVNRevision.isValidRevisionNumber(externalPegRevision.getNumber())) {
	            revisionNumber = externalPegRevision.getNumber();
	        }
	        SVNExternalDetails details = new SVNExternalDetails(externalURL, revisionNumber);

	        externalDetails.put(externalPath, details);
	        return new SVNRevision[] {externalRevision, externalPegRevision};
		}
		
		private static class SVNExternalDetails {
	        private final SVNURL url;
	        private final long revision;

	        private SVNExternalDetails(SVNURL url, long revision) {
	            this.url = url;
	            this.revision = revision;
	        }

	        public SVNURL getUrl() {
	            return url;
	        }

	        public long getRevision() {
	            return revision;
	        }
	    }
	}
}
