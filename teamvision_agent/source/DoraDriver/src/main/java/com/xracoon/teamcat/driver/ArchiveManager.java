package com.xracoon.teamcat.driver;

import java.io.File;

import org.slf4j.Logger;

public interface ArchiveManager{
	void setLogger(Logger logger);
	boolean processArchiveRequest(String file, int type);
	boolean isFileAvailable(File file);
}
