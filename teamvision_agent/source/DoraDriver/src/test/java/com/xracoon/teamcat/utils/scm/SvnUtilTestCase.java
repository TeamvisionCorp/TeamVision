package com.xracoon.teamcat.utils.scm;

import java.util.List;

import org.junit.Test;

import com.xracoon.teamcat.utils.scm.Revision;
import com.xracoon.teamcat.utils.scm.ScmUtil;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class SvnUtilTestCase {
	String url="https://10.14.1.85/svn/qa/UITest/UITest_NGA_4.6Test";
	String user="xxx";
	String passwd="xxx";
	String path="F:/Temp/SCMTest";
	
	@Test
	public void testCheckout() throws Exception{
		ScmUtil scm=ScmUtil.getScm(url, "3990", "F:/Temp/SCMTest", user, passwd.toCharArray(), ScmUtil.SVN_STRATEGY_CHECKOUT);
		scm.checkout();
	}
	
	@Test
	public void testUpdate() throws Exception{
		ScmUtil scm=ScmUtil.getScm(url, null, "F:/Temp/SCMTest", user, passwd.toCharArray(), ScmUtil.SVN_STRATEGY_UPDATE);
		scm.update();
	}
	
	@Test
	public void testVersionAndLog() throws Exception{
		ScmUtil scm=ScmUtil.getScm(url, null, "F:/Temp/SCMTest", user, passwd.toCharArray(), ScmUtil.SVN_STRATEGY_CHECKOUT);
		String version = scm.getVersion();
		List<Revision> logs=scm.getChangeSet("3799");
		int i=logs.size();
		
		JSONObject obj=new JSONObject();
		obj.put("repo", "11111");
		obj.put("changes", JSONArray.fromObject(logs));
		
		System.out.println(obj.toString(2));
	}
}
