package cn.teamcat.doreamon.controller.tools;

import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.net.ssl.SSLContext;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.http.Header;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPatch;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.conn.ssl.TrustStrategy;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;
import org.apache.log4j.Logger;
import com.meterware.httpunit.HttpUnitOptions;
import com.meterware.httpunit.PostMethodWebRequest;
import com.meterware.httpunit.WebConversation;
import com.meterware.httpunit.WebRequest;
import com.meterware.httpunit.javascript.JavaScript.Control;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.app.Launcher;
import cn.teamcat.doreamon.controller.config.GlobalConfig;
import cn.teamcat.doreamon.controller.flow.IssueStatistics;


/**
 * httpclient调用和json的解析
 * 
 * @author Siyuan.Lu
 *
 */
public class HttpClientHelperBasic {

	private static Logger log = Logger.getLogger(HttpClientHelperBasic.class);
    CommonUtil time = new CommonUtil();
	/**
	 * Get请求
	 * 
	 * @param interf
	 * @param param
	 * @return
	 * @throws Exception
	 */
	public static JSONObject get(String url, Map<String, String> params) throws Exception {
		// 取得HttpClient对象
		CloseableHttpClient httpclient = HttpClients.createDefault();
		String param = "";
		if (params != null) {
			if (!params.isEmpty()) {
				Set<?> s = params.keySet();
				Iterator<?> i = s.iterator();
				while (i.hasNext()) {
					Object o = i.next();
					param = param + o + "=" + params.get(o) + "&";
				}
				param = param.substring(0, param.length() - 1);
			}
		}
		String request = url + "?" + param;
		if (param.equals("")) {
			request = request.substring(0, request.length() - 1);
		}
		HttpGet httpget = new HttpGet(request);
		log.info("method:get___测试地址:" + request);
		// 请求HttpClient，取得HttpResponse
		CloseableHttpResponse httpResponse = httpclient.execute(httpget);
		// 请求成功
		log.info("输入参数为:" + param);
		String actual = EntityUtils.toString(httpResponse.getEntity(), "UTF-8");
		log.info(actual);
		return JSONObject.fromObject(actual);
	}

	/**
	 * Post请求
	 * 
	 * @param interf
	 * @param parameters
	 * @return
	 * @throws Exception
	 */
	public static JSONObject post(String url, Map<String, String> params) throws Exception {
		// 定义HttpClient
		CloseableHttpClient httpclient = HttpClients.createDefault();
		// 实例化HTTP方法
		HttpPost httpost = new HttpPost(url);
		List<NameValuePair> nvps = new ArrayList<NameValuePair>();
		Set<String> keySet = params.keySet();
		for (String key : keySet) {
			nvps.add(new BasicNameValuePair(key, params.get(key)));
		}
		httpost.setEntity(new UrlEncodedFormEntity(nvps, "UTF-8"));
		// 执行请求
		HttpResponse httpResponse = httpclient.execute(httpost);
		// 取得返回的字符串
		log.info("++++++method:post++++++request url: "+url);
		log.info("++++++method:post++++++request body: "+params);
		String strResult = EntityUtils.toString(httpResponse.getEntity(), "UTF-8");
		log.info(strResult);
		httpclient.close();
		return JSONObject.fromObject(strResult);
	}
	public static JSONObject postobj(String url,JSONObject jsonObj) throws Exception {
		// 定义HttpClient
		CloseableHttpClient httpclient = HttpClients.createDefault();
		// 实例化HTTP方法
		HttpPost httpost = new HttpPost(url);
		httpost.setHeader("Content-Type", "application/json;charset=UTF-8");
		Header[] headers=httpost.getAllHeaders();
		log.info("++++++++++++++++++++++++headersdetail:"+Arrays.asList(headers)); 
		log.info("++++++method:postobj++++++request url: "+url);
		log.info("++++++method:postobj++++++request body: "+jsonObj);
	    String jsonStr=jsonObj.toString();
	    StringEntity entity=new StringEntity(jsonStr, "UTF-8");
	    httpost.setEntity(entity);      
	    // 执行请求
		HttpResponse httpResponse = httpclient.execute(httpost);			
		//取得返回的字符串                
		String strResult = EntityUtils.toString(httpResponse.getEntity(), "UTF-8"); 
		Header[] header =httpResponse.getAllHeaders(); 
		System.out.println("接口返回值中所带的header为：" +header.toString());
		httpclient.close(); 
		return JSONObject.fromObject(strResult); 
	}
	public static JSONObject putobj(String url,JSONObject jsonObj) throws Exception {
		// 定义HttpClient
		CloseableHttpClient httpclient = HttpClients.createDefault();
		// 实例化HTTP方法
		HttpPut httpput = new HttpPut(url);
		//post增加head头信息
		//httpost.setHeader("UserKey", "application/json;charset=UTF-8");
		httpput.setHeader("Content-Type", "application/json;charset=UTF-8");
		Header[] headers=httpput.getAllHeaders();
		log.info("++++++++++++++++++++++++headersdetail:"+Arrays.asList(headers)); 
		log.info("++++++method:put++++++request url: "+url);
		log.info("++++++method:put++++++request body: "+jsonObj);
	    String jsonStr=jsonObj.toString();
	    StringEntity entity=new StringEntity(jsonStr, "UTF-8");
	    httpput.setEntity(entity);      
	    // 执行请求
		HttpResponse httpResponse = httpclient.execute(httpput);			
		//取得返回的字符串                
		String strResult = EntityUtils.toString(httpResponse.getEntity(), "UTF-8"); 
		httpclient.close(); 
		return JSONObject.fromObject(strResult);            			
	}
	
	public static JSONObject patchobj(String url,JSONObject jsonObj) throws Exception {
		// 定义HttpClient
		CloseableHttpClient httpclient = HttpClients.createDefault();
		// 实例化HTTP方法
		HttpPatch httpPatch = new HttpPatch(url); 
		//post增加head头信息
		//httpost.setHeader("UserKey", "application/json;charset=UTF-8");
		httpPatch.setHeader("Content-Type", "application/json;charset=UTF-8");
		Header[] headers=httpPatch.getAllHeaders();
		log.info("++++++++++++++++++++++++headersdetail:"+Arrays.asList(headers)); 
		log.info("++++++method:dpatch++++++request url: "+url);
		log.info("++++++method:dpatch++++++request body: "+jsonObj);
	    String jsonStr=jsonObj.toString();
	    log.info("请求参数为"+jsonStr);
	    StringEntity entity=new StringEntity(jsonStr, "UTF-8");
	    httpPatch.setEntity(entity);      
	    // 执行请求
		HttpResponse httpResponse = httpclient.execute(httpPatch);	

		//取得返回的字符串                
		String strResult = EntityUtils.toString(httpResponse.getEntity(), "UTF-8"); 
		httpclient.close(); 
		log.info("请求返回值为"+JSONObject.fromObject(strResult));
		return JSONObject.fromObject(strResult);            			
	}
	
	public static JSONObject deleteobj(String url,JSONObject jsonObj) throws Exception {
		// 定义HttpClient
		CloseableHttpClient httpclient = HttpClients.createDefault();
		// 实例化HTTP方法
		 HttpDeleteWithBody httpdelete = new HttpDeleteWithBody(url);
		//post增加head头信息
		//httpost.setHeader("UserKey", "application/json;charset=UTF-8");
		 httpdelete.setHeader("Content-Type", "application/json;charset=UTF-8");
		Header[] headers=httpdelete.getAllHeaders();
		log.info("++++++++++++++++++++++++headersdetail:"+Arrays.asList(headers)); 
		log.info("++++++method:deleteobj++++++request url: "+url);
		log.info("++++++method:deleteobj++++++request body: "+jsonObj);
	    String jsonStr=jsonObj.toString();
	    StringEntity entity=new StringEntity(jsonStr, "UTF-8");
	    httpdelete.setEntity(entity);      
	    // 执行请求
		HttpResponse httpResponse = httpclient.execute(httpdelete);			
		//取得返回的字符串                
		String strResult = EntityUtils.toString(httpResponse.getEntity(), "UTF-8"); 
		httpclient.close(); 
		return JSONObject.fromObject(strResult);            			
	}
	
	public static void delete(String url) throws Exception {
		// 定义HttpClient
		CloseableHttpClient httpclient = HttpClients.createDefault();
		// 实例化HTTP方法
		 HttpDeleteWithBody httpdelete = new HttpDeleteWithBody(url);
		//post增加head头信息
		//httpost.setHeader("UserKey", "application/json;charset=UTF-8");
		 httpdelete.setHeader("Content-Type", "application/json;charset=UTF-8");
		Header[] headers=httpdelete.getAllHeaders();
		log.info("++++++++++++++++++++++++headersdetail:"+Arrays.asList(headers)); 
		log.info("++++method:delete++++++++request url: "+url);      
	    // 执行请求
		httpclient.execute(httpdelete);			
		//取得返回的字符串                
		httpclient.close();            			
	}
	
}