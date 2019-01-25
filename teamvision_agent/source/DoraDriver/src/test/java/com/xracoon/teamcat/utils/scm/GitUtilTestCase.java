package com.xracoon.teamcat.utils.scm;

import java.util.List;

import org.junit.Test;

import com.xracoon.teamcat.utils.scm.CmdGitUtil;
import com.xracoon.teamcat.utils.scm.Revision;
import com.xracoon.teamcat.utils.scm.ScmUtil;

public class GitUtilTestCase {
	String url="http://10.14.1.85/ios/ESports.git" ;//"https://bitbucket.org/tx-personal/apple-skep.git";
	String user="xxxx";
	String passwd="xxxx";
	String path="F:/Temp/GitTest";
	String oldRev="fe39a8130fc7";
	//String oldRevFull="fe39a8130fc7cffbc4f6d16c0a09cdc8b1b0de3b";
	String branch="master";
	
	@Test
	public void testCheckout() throws Exception{
		ScmUtil scm=ScmUtil.getScm(url, branch, path, user, passwd.toCharArray(), ScmUtil.GIT_STRATEGY_SHALLOW_CLONE);
		scm.checkout();
	}
	
	@Test
	public void testCmdGitCheckout() throws Exception{
		CmdGitUtil scm=(CmdGitUtil) ScmUtil.getScm(url, branch, path, user, passwd.toCharArray(), ScmUtil.GIT_STRATEGY_SHALLOW_CLONE);
		scm.checkout();
	}
	
	@Test
	public void testUpdate() throws Exception{
		ScmUtil scm=ScmUtil.getScm(url, branch, path, user, passwd.toCharArray(), ScmUtil.GIT_STRATEGY_UPDATE);
		scm.update();
	}
	
	@Test
	public void testVersionAndLog() throws Exception{
		ScmUtil scm=ScmUtil.getScm(url, null, path, user, passwd.toCharArray(), ScmUtil.GIT_STRATEGY_UPDATE);
		scm.exec();
		String version = scm.getVersion();
		List<Revision> logs=scm.getChangeSet(oldRev);
		int i=logs.size();
	}
}
