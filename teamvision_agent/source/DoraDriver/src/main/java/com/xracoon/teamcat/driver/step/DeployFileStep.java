package com.xracoon.teamcat.driver.step;

import java.io.File;
import java.io.FileInputStream;
import java.util.Map;

import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.utils.HttpUtils;

public class DeployFileStep extends DeployStep {
	@Override
	public boolean depoyExec() throws Exception {
		//替换文件
		Map<Long, DeployFileItem> replaceFiles= WebService.queryDeployReplaceFile(deployInfo.getId());
		for(DeployFileItem f:replaceFiles.values()){
			if(f.replaceTarget==null || f.replaceTarget.equalsIgnoreCase("null"))
				continue;
			
			String url=WebService.baseUrlCI.substring(0,WebService.baseUrlCI.length()-7)+f.fileUrl.substring(f.fileUrl.indexOf("/ci/"));
			String localfile=new File(this.loalDepoyTempDir, f.fileName).toString();
			String remotefile=new File(this.remotePath, f.replaceTarget).toString().replace("\\", "/");
			HttpUtils.download(url, localfile);
			sshUtil.writeFile(new FileInputStream(localfile), remotefile);
			logger.info("replace file: "+localfile+ " -> "+ remotefile);
		}
		
		return true;
	}
	
	public static class DeployFileItem{
		private long fileId;
		private String fileUrl;
		private String fileName;
		private String replaceTarget;
		
		public DeployFileItem(){}
		public DeployFileItem(long id, String url, String name, String replace){
			this.fileId=id;
			this.fileUrl=url;
			this.fileName=name;
			this.replaceTarget=replace;
			if(replace!=null && replace.equalsIgnoreCase("null"))
				this.replaceTarget=null;
		}
		public long getFileId() {
			return fileId;
		}
		public void setFileId(long fileId) {
			this.fileId = fileId;
		}
		public String getFileUrl() {
			return fileUrl;
		}
		public void setFileUrl(String fileUrl) {
			this.fileUrl = fileUrl;
		}
		public String getFileName() {
			return fileName;
		}
		public void setFileName(String fileName) {
			this.fileName = fileName;
		}
		public String getReplaceTarget() {
			return replaceTarget;
		}
		public void setReplaceTarget(String replaceTarget) {
			this.replaceTarget = replaceTarget;
		}
	}


}
