package com.xracoon.teamcat.driver;

import com.xracoon.teamcat.driver.step.BuildStep;
import com.xracoon.teamcat.driver.step.BuildStep.StepType;
import com.xracoon.teamcat.driver.step.ScmStep;
import com.xracoon.teamcat.driver.step.ShellPackageStep;
import com.xracoon.teamcat.driver.step.testngsteps.TestNgInterfaceStep;
import com.xracoon.teamcat.driver.step.testngsteps.TestNgWebUiStep;
import com.xracoon.teamcat.plugin.TaskConfig;
import com.xracoon.teamcat.plugin.TaskSection;
import com.xracoon.teamcat.plugin.TaskStep;
import com.xracoon.teamcat.utils.scm.Revision;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.OS;

import java.util.Date;
import java.util.List;
import java.util.Map;

public class StepDriver extends Driver {
	private BuildStep currentStep;

	@Override
	public boolean init() {
		this.isInit = true;
		return true;
	}

	@Override
	public boolean exec() {
		try {
			StepType.PACKAGE_CMD.setHandler(ShellPackageStep.class.getName());
			StepType.TEST_INTERFACE.setHandler(TestNgInterfaceStep.class.getName());
			StepType.WEBUI_TEST.setHandler(TestNgWebUiStep.class.getName());

			if (this.getNotifier() == null)
				throw new Exception("agent notifier is null");

			if (!this.isInit)
				throw new Exception("driver does't have be initialized");

			OS os = OS.getSingleton().clone();
			os.setLogger(logger);

			List<TaskStep> steps = this.getTaskConfig().getAllSteps();
			TaskStep lastScmStep = steps.size() > 0 ? steps.get(steps.size() - 1) : null;
			TaskSection scmSection = this.getTaskConfig().getSection(TaskConfig.SECTION_SCM);
			int scmStepNum = -1;
			if (scmSection != null && scmSection.getSteps() != null && (scmStepNum = scmSection.getSteps().size()) > 0)
				lastScmStep = scmSection.getSteps().get(scmStepNum - 1);
			int scmIdx = 0;
			for (TaskStep step : steps) {
				step.resolveTokens(getTokens());
				step.logDesc();
				if (step.getType() == StepType.SCM_SVN || step.getType() == StepType.SCM_GIT)
					scmIdx++;

				if (!step.isEnable()) {
					if (step.getType() != StepType.BASIC_INFO)
						logger.info("skip disable step " + step.getType().getName());
					continue;
				}

				Date start = new Date();
				try {
//					step.resolveTokens(getTokens());
					BuildStep stepHandler = BuildStep.fromTask(step, env);
					currentStep = stepHandler;
					if (stepHandler instanceof ScmStep)
						env.put(Driver.ENV_SCMSTEPIDX, scmIdx);
					if (!stepHandler.exec()) {
						throw new Exception("Step failed: " + " Step : {'name': '" + step.getType().getName()
								+ "', 'order':'" + step.getOrder() + "', 'section':'" + step.getSectionName() + "'}"); // 错误
					}
				} catch (Exception e) {
					throw e;
				} finally {
					currentStep = null;
					if (start != null) {
						long duration = new Date().getTime() - start.getTime();
						logger.info("----------------------------------------------------------");
						logger.info("Summary: {'section':'" + step.getSectionName() + "','order':'" + step.getOrder()
								+ "', 'duraMs':" + duration + ", 'duraDesc':'" + StringEx.dateRangeDesc(duration)
								+ "'}");
						logger.info("----------------------------------------------------------");
						logger.info("");
					}
					if (step == lastScmStep) {
						logger.info("");
						logger.info("----------------------------------------------------------");
						logger.info("update history infomation");
						logger.info("----------------------------------------------------------");
						// 更新SCM
						updateHistoryInfo(env);
					}
					String packageInfo = (String) env.get(Driver.ENV_PACKAGEINFO);
					if (packageInfo != "") {
						updatePackageInfo(env);
					}
				}
			}

			updatePackageInfo(env);
			// @SuppressWarnings("unchecked")
			// Map<String,String> driverArgs=(Map<String,String>)
			// options.get(DriverArg.DRIVERARG);
			// return build(workspace,driverArgs);

			return true;
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
			String msg = e.getMessage();
			if (msg == null || msg.trim().length() == 0)
				msg = e.getStackTrace()[0].toString();
			this.setMessage("StepDriver Runtime Error: " + msg);
			return false;
		}
	}

	public void updatePackageInfo(Map<String, Object> options) throws Exception {
		String packageInfo = (String) options.get(Driver.ENV_PACKAGEINFO);
		long historyID = (long) options.get(Driver.ENV_HISTORYID);
		boolean result = WebService.updateHistoryData(historyID, null, null, packageInfo);
		logger.info("update package info -> package info :" + packageInfo);
		logger.info("update package info result: " + result);
	}

	public void updateHistoryInfo(Map<String, Object> options) throws Exception {
		@SuppressWarnings("unchecked")
		Map<String, String> versionMap = (Map<String, String>) options.get(Driver.ENV_VERSIONMAP);
		@SuppressWarnings("unchecked")
		Map<String, List<Revision>> changeMap = (Map<String, List<Revision>>) options.get(Driver.ENV_CHANGESET);

		long historyID = (long) options.get(Driver.ENV_HISTORYID);
		logger.info("update history info -> last version :" + (versionMap != null ? versionMap.toString() : ""));
		logger.info("update hsitory info -> change set :" + (changeMap != null ? changeMap.toString() : ""));

		boolean result = WebService.updateHistoryData(historyID, versionMap, changeMap, null);
		logger.info("update history info result: " + result);
	}

	@Override
	public boolean stop() {
		logger.warn("Driver Interupted");// cmd /k start taskkill /f /im cmd.exe

		return true;
	}

	@Override
	public String[] getArgsDesc() {
		String[] argsDes = new String[1];
		// argsDes[0]="testngRelatPath=relate path of directory which contains
		// testng.xml";
		return argsDes;
	}
}
