package com.xracoon.teamcat.driver.step.testngsteps;

import com.xracoon.teamcat.driver.BuildTools;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.driver.WebService.CaseMapItem;
import com.xracoon.teamcat.models.ci.CiAutoCaseInfo;
import com.xracoon.teamcat.models.ci.CiTaskBasic;
import com.xracoon.teamcat.utils.testngtools.caseparser.TestSuiteBuilder;
import com.xracoon.teamcat.utils.testngtools.caserunner.TestConfigTool;
import com.xracoon.teamcat.utils.testngtools.caserunner.TestngRunner;
import com.xracoon.teamcat.utils.testngtools.resultparser.TestngReportTool;
import com.xracoon.teamcat.plugin.TaskConfig;
import com.xracoon.testutil.model.TestCase;
import com.xracoon.testutil.model.TestSuite;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.ExecStatus;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class TestNgInterfaceStep extends TestNgStep {
	private TestSuite testSuite=null;
	private TestngRunner testRunner;
	private String projectDir;
	private String outputFilter;
	private List<TestCase> cases;
	private Map<String, CaseMapItem> caseIdMap;

	@Override
	public void initEnv() throws Exception {
		String jdk=stepConf.getParam("auto_tool_jdk");
		String envId=stepConf.getParam("auto_host_info");
		projectDir= stepConf.getParam("auto_project_dir");
		outputFilter=stepConf.getParam("auto_log_dir");
		String caseTag = stepConf.getParam("autocase_filter");
		this.cleanOutput(outputFilter);

		//locate tools
		BuildTools bt=(BuildTools) env.get(Driver.ENV_BUILDTOOLS);
		File jdkPath=bt.getJDKPath(jdk);

		//query case
		//caseIdMap= WebService.queryCaseResultsIdMap(Long.parseLong(env.get(Driver.ENV_TESTRESULTID).toString()));

		TaskConfig taskConfig= (TaskConfig) env.get(Driver.ENV_TASKCONFIG);
		//prepare host
		if(!StringEx.isBlank(envId) && StringEx.isNumber(envId))
			prepareHost(Integer.parseInt(envId));
		Map<String,Object> taskQueueInfo = WebService.queryTaskQueueInfo(taskConfig.getTaskQueueId());
		CiTaskBasic ciTaskBasic=WebService.queryTaskBasic((Integer)taskQueueInfo.get("TaskID"));
		Map<String,String> params = new HashMap<>();
		params.put("ProjectID",ciTaskBasic.getResult().getProject().toString());
		params.put("CaseType",Driver.TEST_CASE_TYPE_INTERFACE);
		params.put("CaseTag",caseTag);
		params.put("page_size",Integer.MAX_VALUE+"");
		CiAutoCaseInfo ciAutoCaseInfo=WebService.queryAutoCases(params);
		//String caseIds= WebService.queryTaskQueueInfo(taskConfig.getTaskQueueId()).get("CaseList").toString();
		logger.info("AutoCaseInfo: "+ciAutoCaseInfo.toString());
		if(ciAutoCaseInfo.getResult().getResults().size()==0)
			throw new Exception("未查询到CaseList");
		caseIdMap=getCaseMapItemByCiAutoCaseInfo(ciAutoCaseInfo);
		cases= getTestCaseIdsByCiTaskBasic(ciAutoCaseInfo);
	}

	@Override
	public boolean runTest() throws Exception {
		String testngxmlFilePath=workspace+"/"+projectDir;
		String testOutputPath=testngxmlFilePath+"/target/surefire-reports";

		testSuite = TestSuiteBuilder.parseToSuiteOfCases(cases);
		TestConfigTool.setLogger(logger);
		TestConfigTool.createConfigFile(testSuite, testngxmlFilePath);

		logger.info("run test... ");

		//------------
		testRunner=new TestngRunner();
		testRunner.setLogger(logger);
		ExecStatus status=testRunner.start(testngxmlFilePath);

		if(status.getRetVal()!=0){
			throw new Exception("Maven Error: "+status.getError());
			//this.setMessage("InterfaceDriver Runtime Error: "+status.getError());
		}

		logger.info("parser result...");
		TestngReportTool  parser=new TestngReportTool();
		parser.addTestListener(new TestListenerImpl(caseIdMap));
		parser.setLogger(logger);
		parser.parseTestngResults(testOutputPath);
		return true;
	}

	@Override
	public boolean runFinsh() throws Exception{

		return this.archiveFiles(outputFilter, Driver.ARCHIVE_LOG);
	}

}
