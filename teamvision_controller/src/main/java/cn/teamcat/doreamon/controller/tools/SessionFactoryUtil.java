package cn.teamcat.doreamon.controller.tools;

import java.io.IOException;
import java.io.InputStream;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionManager;

public class SessionFactoryUtil {
	static public SqlSessionManager sessionManager=null;
	
	static {
		initSessionFactory();
	}
	
	public static void initSessionFactory()
	{
		String resource = "mybatis-config.xml";
		InputStream inputStream;
		try {
			inputStream = Resources.getResourceAsStream(resource);
			sessionManager=SqlSessionManager.newInstance(inputStream);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	static public SqlSession newSession()
	{
		return sessionManager.openSession(true);
	}
	
	static public SqlSession getSession()
	{
		if(!sessionManager.isManagedSessionStarted())
			sessionManager.startManagedSession(true);
		return sessionManager;
	}
}
