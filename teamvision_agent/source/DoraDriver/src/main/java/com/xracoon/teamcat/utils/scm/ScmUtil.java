package com.xracoon.teamcat.utils.scm;

import java.io.File;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public abstract class ScmUtil {
	protected Logger logger = LoggerFactory.getLogger(ScmUtil.class);
	public void setLogger(Logger logger){
		this.logger=logger;
	}
	
	public static final int SVN_STRATEGY_CHECKOUT=1;
	public static final int SVN_STRATEGY_UPDATE=2;
	public static final int GIT_STRATEGY_FULL_CLONE=2;
	public static final int GIT_STRATEGY_SHALLOW_CLONE=1;
	public static final int GIT_STRATEGY_UPDATE=3;
	
	protected String repository;
	protected File path;
	protected String userName;
	protected char[] password;
	protected String branchOrVersion;
	protected int strategy;
	protected boolean keepCredential=false;
	
	protected ScmUtil(String url,String branchOrVersion,String localPath,String userName,char[] password, int strategy){
		this.repository = url;
		this.branchOrVersion = branchOrVersion;
		this.path = new File(localPath);
		this.userName = userName;
		this.password = password;
		this.strategy=strategy;
	}
	
	protected ScmUtil(){}
	
	public static ScmUtil getScm(String url,String branchOrVersion,String localPath,String userName,char[] password, int strategy) throws Exception{
		ScmUtil scm = null;
		if(url.contains(".git"))
			scm = new CmdGitUtil(url, branchOrVersion, localPath, userName, password, strategy);
		else {
			scm = new SvnUtil(url, branchOrVersion, localPath, userName, password, strategy);
		}
		return scm;
	}
	
	public abstract boolean exec() throws Exception;
	public abstract boolean checkout()throws Exception;
	public abstract boolean update()throws Exception;
	public abstract String getVersion();
	public abstract List<Revision> getChangeSet(String untilToVersion);
}
