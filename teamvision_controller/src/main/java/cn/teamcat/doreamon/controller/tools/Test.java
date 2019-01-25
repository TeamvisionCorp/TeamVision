package cn.teamcat.doreamon.controller.tools;

import org.apache.log4j.chainsaw.Main;

import net.sf.json.JSONObject;


public class Test{
	public static void main(String[] args) {
        String cmd = "{\"channel\":\"test\",\"message\":\"{\"tq_id\":\"1\",\"test_result_id\":\"123\"}\"}";
		System.out.println("cmd为："+cmd);
		try {
			HttpClientHelper.postMq("test",cmd);
		} catch (Exception e) {
			// TODO: handle exception
		}
		
	
	}
	
}