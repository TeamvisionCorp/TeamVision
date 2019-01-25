package com.xracoon.teamcat.agent.network;

import java.io.File;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ReAliveChecker implements Runnable {
	private Logger logger=LoggerFactory.getLogger(ReAliveChecker.class);
	private long limit=1000*60*2; //2 min
	private StatusUpdater infoUpdater;
	
	public ReAliveChecker(StatusUpdater infoUpdater, int interval){
		this.infoUpdater=infoUpdater;
		this.limit=interval;
	}
	
	@Override
	public void run() {
		File lastAliveFile=new File("lastAlive");
		
		while(true){
			try {
				Thread.sleep(limit);
			} catch (InterruptedException e) {
				break;
			}
			if(lastAliveFile!=null){
				if(System.currentTimeMillis()-lastAliveFile.lastModified()>limit){
					logger.warn("!! Can not get sync signal from controller in "+limit/1000+" seconds. Agent try to update to alive status again");
					infoUpdater.upateStatus();
				}
			}
		}
	}
}
