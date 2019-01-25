package com.xracoon.teamcat.agent.device;

public interface Execution {
	boolean isAlive();
	void stop();
	void waitFor() throws InterruptedException;
	String getOutput();
}
