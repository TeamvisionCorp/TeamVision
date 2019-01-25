package com.xracoon.teamcat.driver.step;

public abstract class TestStep extends BuildStep {
	@Override
	public final boolean exec() throws Exception {
		return execTest();
	}
	
	public abstract boolean execTest() throws Exception;
}
