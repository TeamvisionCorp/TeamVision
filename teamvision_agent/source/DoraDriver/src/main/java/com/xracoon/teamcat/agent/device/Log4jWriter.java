package com.xracoon.teamcat.agent.device;

import java.io.IOException;
import java.io.Writer;

import org.apache.log4j.Logger;

public class Log4jWriter extends Writer {
	private Logger logger = Logger.getLogger("Log4jWriter");
	public Log4jWriter(){}
	public Log4jWriter(Logger logger)
	{
		this.logger=logger;
	}
	
	@Override
	public void write(char[] cbuf, int off, int len) throws IOException {
		String info=new String(cbuf, off, len).trim();
		if(info.length()>0)
			logger.info(info.trim());
	}

	@Override
	public void flush() throws IOException {
	}

	@Override
	public void close() throws IOException {
	}

}
