package com.xracoon.teamcat.utils.testngtools;

import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestClass;
import com.xracoon.testutil.model.TestPack;
import com.xracoon.testutil.model.TestSuite;

import java.util.EventListener;

public interface TestProcessListener extends EventListener {
	void prepare(TestSuite suite);
	
	void start(TestCase tcase);
	void end(TestCase tcase) throws Exception;
	
	void start(TestClass tclass);
	void end(TestClass tclass);
	
	void start(TestPack tclass);
	void end(TestPack tclass);
	
	void start(TestSuite tclass);
	void end(TestSuite tclass);
	
	void finish(TestSuite suite);
}
