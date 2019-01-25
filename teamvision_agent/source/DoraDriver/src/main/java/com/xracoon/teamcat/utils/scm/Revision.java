package com.xracoon.teamcat.utils.scm;

import java.util.List;

public class Revision{
	private String version;
	private String author;
	private String authorEmail;
	private String timestamp;
	private String message;
	private List<Change> changes;
	
	public Revision(){}
	public Revision(String v, String a, String e, String t, String m, List<Change> changes){
		this.version=v;
		this.author=a;
		this.authorEmail=e;
		this.timestamp=t;
		this.message=m;
		this.changes=changes;
	}
	public String getVersion() {
		return version;
	}
	public void setVersion(String version) {
		this.version = version;
	}
	public String getAuthor() {
		return author;
	}
	public void setAuthor(String author) {
		this.author = author;
	}
	public String getTimestamp() {
		return timestamp;
	}
	public void setTimestamp(String timestamp) {
		this.timestamp = timestamp;
	}
	public String getMessage() {
		return message;
	}
	public void setMessage(String message) {
		this.message = message;
	}
	public List<Change> getChanges() {
		return changes;
	}
	public void setChanges(List<Change> changes) {
		this.changes = changes;
	}
	public String getAuthorEmail() {
		return authorEmail;
	}
	public void setAuthorEmail(String authorEmail) {
		this.authorEmail = authorEmail;
	}
}
