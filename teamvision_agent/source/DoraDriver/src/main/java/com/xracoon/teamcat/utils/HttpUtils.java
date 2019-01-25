package com.xracoon.teamcat.utils;

import java.io.File;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import org.apache.http.Consts;
import org.apache.http.HttpEntity;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPatch;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.client.methods.HttpRequestBase;
import org.apache.http.client.utils.URIBuilder;
import org.apache.http.entity.ContentType;
import org.apache.http.entity.StringEntity;
import org.apache.http.entity.mime.MultipartEntityBuilder;
import org.apache.http.entity.mime.content.FileBody;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;

import net.sf.json.JSONObject;

public class HttpUtils {
	
	/**
	 * 发请求
	 * @param urlParams
	 * @param url
	 * @return
	 * @throws Exception
	 */
	public static CloseableHttpResponse httpRequest(String url, String method, Map<String, String> urlParams, Map<String,String> headers,boolean multipart) throws Exception {
		CloseableHttpClient httpclient = HttpClients.createDefault();
		HttpRequestBase req=null;
		method=method.toUpperCase();
		
		URIBuilder builder=new URIBuilder(url);
		if(urlParams!=null && urlParams.size()>0){
			List<NameValuePair> params=new ArrayList<>();
			for(Entry<String,String> e:urlParams.entrySet())
				params.add(new BasicNameValuePair(e.getKey(),e.getValue()));
			builder.addParameters(params);
		}
		
		if(method.equals("GET")){
			req=new HttpGet(builder.build());
		}
		else if(method.equals("POST")){
			HttpPost postReq=new HttpPost(url);
			HttpEntity entity=null;
			if(multipart){
				MultipartEntityBuilder meb=MultipartEntityBuilder.create();
				for(NameValuePair param:builder.getQueryParams())
					if(new File(param.getValue()).exists())
						meb.addPart(param.getName(),new FileBody(new File(param.getValue())));
					else
						meb.addTextBody(param.getName(), param.getValue(),ContentType.create("text/plain", Consts.UTF_8));
				entity=meb.build();
			}else
			entity=new UrlEncodedFormEntity(builder.getQueryParams(), Consts.UTF_8);  //Url编码
			
			postReq.setEntity(entity);
			req=postReq;
		}
		//Content-Type:application/json; Charset: utf-8
		else if(method.equals("PATCH")){
			HttpPatch reqPatch=new HttpPatch(url);
			String json=JSONObject.fromObject(urlParams).toString();
			StringEntity entity = new StringEntity(json, ContentType.create("application/json", Consts.UTF_8)); 
			reqPatch.setEntity(entity);
			req=reqPatch;
		}else if(method.equals("PUT")){
			HttpPut reqPatch=new HttpPut(url);
			String json=JSONObject.fromObject(urlParams).toString();
			StringEntity entity = new StringEntity(json, ContentType.create("application/json", Consts.UTF_8)); 
			//HttpEntity entity=new UrlEncodedFormEntity(builder.getQueryParams(), Consts.UTF_8);
			reqPatch.setEntity(entity);
			req=reqPatch;
		}
		
		if(req==null)
			return null;
		
		if(headers!=null && headers.size()>0){	
			for(Entry<String,String> e:headers.entrySet())
				req.addHeader(e.getKey(), e.getValue());
		}
		
		//Builder requestConfigBuilder = RequestConfig.custom();
		//requestConfigBuilder.setConnectionRequestTimeout(1000).setMaxRedirects(1);
		//req.setConfig(requestConfigBuilder.build());
		
		CloseableHttpResponse response = httpclient.execute(req);
		return response;
	}
	
	public static void download(String url, String path) throws Exception{
		CloseableHttpResponse response = HttpUtils.httpRequest(url, "GET", null, null, false);
		File file=new File(path);
		if(!file.exists() && !file.getParentFile().exists())
			file.getParentFile().mkdirs();
		
		FileOutputStream fos=new FileOutputStream(path);
		try{
			response.getEntity().writeTo(fos);
		}
		catch(Exception e){
			throw e;
		}
		finally{
			if(fos!=null)
				fos.close();
		}
	}
	
//	public static WebResponse sendRequest(String url, String method, Map<String, String> urlParams, Map<String,String> headers,boolean multipart) throws Exception {
//		HttpUnitOptions.setDefaultCharacterSet("UTF-8");
//		WebConversation conn=new WebConversation();
//		WebRequest req=null;
//		
//		method=method.toUpperCase();
//		if(method.equals("GET")){
//			req=new GetMethodWebRequest(url);
//			
//		}
//		else if(method.equals("POST")){
//			req=new PostMethodWebRequest(url);
//		}
//		
//		if(req==null)
//			return null;
//		
//		if(urlParams!=null && urlParams.size()>0){
//			for(Entry<String,String> e:urlParams.entrySet()){
//				if(method.equals("POST") && multipart && new File(e.getValue()).exists())
//					req.selectFile(e.getKey(), new File(e.getValue()));
//				else
//					req.setParameter(e.getKey(), e.getValue());
//			}
//		}
//		
//		if(headers!=null && headers.size()>0){	
//			for(Entry<String,String> e:headers.entrySet())
//				req.setHeaderField(e.getKey(), e.getValue());
//		}
//
//		WebResponse response = conn.getResponse(req);
//		return response;
//	}
	
//	@Deprecated
//	public static void sendRequest0(String url, String method, Map<String, String> urlParams, Map<String,String> headers,boolean multipart){
//		DataOutputStream output=null;
//		HttpURLConnection conn=null;
//		URL uri;
//		try{
//			uri=new URL(url);
//			conn=(HttpURLConnection)uri.openConnection();
//			conn.setDoInput(true);
//			conn.setDoOutput(true);
//			conn.setUseCaches(true);
//			conn.setRequestMethod(method);
//			conn.setRequestProperty("connection", "keep-alive");
//			conn.setRequestProperty("Charset", "UTF-8");
//			//conn.setRequestProperty("Content-Type", "UTF-8");
//		}catch(Exception e){
//			
//		}
//	}
	
}
