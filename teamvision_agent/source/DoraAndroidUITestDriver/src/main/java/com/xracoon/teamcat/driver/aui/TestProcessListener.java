package com.xracoon.teamcat.driver.aui;

import java.util.EventListener;

import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestPack;
import com.xracoon.testutil.model.TestSuite;

public interface TestProcessListener extends EventListener {
	void prepare(TestSuite suite);
	
	void start(TestCase tcase);
	void end(TestCase tcase);
	
	void start(TestClass tclass);
	void end(TestClass tclass);
	
	void start(TestPack tclass);
	void end(TestPack tclass);
	
	void start(TestSuite tclass);
	void end(TestSuite tclass);
	
	void finish(TestSuite suite);
}
