package com.xracoon.teamcat.agent.archive;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.net.SocketException;
import java.util.Date;
import org.apache.commons.net.ftp.FTPClient;
import org.apache.commons.net.ftp.FTPFile;
import org.apache.http.client.utils.DateUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.driver.ArchiveManager;
import com.xracoon.teamcat.driver.TaskInfo;

public  class FtpArchiveManager implements ArchiveManager {
	private Logger logger = LoggerFactory.getLogger(FtpArchiveManager.class);
	private String ip;
	private int port;
	private String user;
	private String passwd;
	private FTPClient client;
	private TaskInfo info;
	private String archiveRoot;
	
	@Override
	public void setLogger(Logger logger){
		this.logger=logger;
	}
	
	public FtpArchiveManager(TaskInfo info, String ip, int port, String user, String passwd, String archiveRoot){
		this.info=info;
		this.ip=ip;
		this.port=port;
		this.user=user;
		this.passwd=passwd;
		this.archiveRoot=archiveRoot;
	}
	
	public boolean openConnection() throws SocketException, IOException{
		client=new FTPClient();
		client.connect(ip, port);
		client.enterLocalPassiveMode();
		//client.setBufferSize(1024);
		return client.login(user, passwd);
	}
	
	public void closeConnection()
	{
		try {
			if(client!=null && client.isConnected())
				client.disconnect();
			client=null;
		} catch (IOException e) {
			logger.error(e.getMessage(), e);
		}
	}
		
	public boolean cleanDirectory(String pathname) throws IOException
	{
		boolean ret=true;
		FTPFile[] files = client.listFiles(pathname);
		for (FTPFile f : files) {
			if (f.isDirectory()) {
				deleteRecursive(pathname + "/" + f.getName());
				ret &=client.removeDirectory(pathname);
			}
			if (f.isFile()) {
				ret &=client.deleteFile(pathname + "/" + f.getName());
			}
		}
		return ret;
	}
	
	public boolean deleteRecursive(String pathname) throws IOException
	{
		cleanDirectory(pathname);
		return client.removeDirectory(pathname);
	}
	
	public boolean upload(String remoteFile, String localFile)
	{
		FileInputStream fis=null;
		try {
			File file=new File(remoteFile);
			String parent=file.getParent();
			if(parent!=null)
			{
				parent=new String(parent.getBytes("GBK"),"iso-8859-1");
				client.makeDirectory(parent);
			}
	        
			fis = new FileInputStream(localFile);			
			client.setFileType(FTPClient.BINARY_FILE_TYPE);
			remoteFile= new String(remoteFile.getBytes("GBK"),"iso-8859-1");
			return client.storeFile(remoteFile, fis);
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
			return false;
		}
		finally
		{
			try {
				client.setFileType(FTPClient.ASCII_FILE_TYPE);
				if(fis!=null)
					fis.close();
			} catch (IOException e1) {
				logger.error(e1.getMessage(), e1);
			}
		}
	}
	
	public boolean isFileAvailable(File file)
	{
/*		if(file.length()==0)
		{
			logger.info(file.getName()+":  size is 0");
			return false;
		}
		else*/ if(file.length()>52428800)
		{
			logger.info(file.getName()+":  too large (>50M)");
			return false;
		}	
		
		return true;
	}
	
	@Override
	public boolean processArchiveRequest(String file, int type) {
		try {
			String remotePath=archiveRoot+"/"+info.taskID+"_"+info.taskConfig.getTaskName()+"/"+DateUtils.formatDate(new Date(), "yyyyMMddHHmmss");
			if(openConnection())
			{
				client.changeWorkingDirectory("/");
				
				//if reomtePath not existed, create it, else do nothing
				client.makeDirectory(remotePath);
				//cleanDirectory(remotePath);
				
				File f=new File(file);
				if(f.exists() && isFileAvailable(f)){
					String remoteFile=remotePath+"/"+file;
					logger.info("upload:  "+file+" ("+file.length()+")");
					boolean ret=upload(remoteFile, file);
					logger.info("upload:  " +ret+"  "+file+"==>"+remoteFile);
				}
				
				return true;
			}
			return false;
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
			return false;
		}
		finally
		{
			closeConnection();
		}
	}
}
