package com.xracoon.teamcat.driver.step;

public class DeployServerInfo {
	private long id;
	private String serverName;
	private String host;
	private String remoteDir;
	private int port;
	private long credentialId;
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public String getServerName() {
		return serverName;
	}
	public void setServerName(String serverName) {
		this.serverName = serverName;
	}
	public String getHost() {
		return host;
	}
	public void setHost(String host) {
		this.host = host;
	}
	public String getRemoteDir() {
		return remoteDir;
	}
	public void setRemoteDir(String remoteDir) {
		this.remoteDir = remoteDir;
	}
	public int getPort() {
		return port;
	}
	public void setPort(int port) {
		this.port = port;
	}
	public long getCredentialId() {
		return credentialId;
	}
	public void setCredentialId(long credentialId) {
		this.credentialId = credentialId;
	}
}
