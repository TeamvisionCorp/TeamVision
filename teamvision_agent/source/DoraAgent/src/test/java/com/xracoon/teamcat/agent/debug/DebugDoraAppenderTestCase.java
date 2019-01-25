package com.xracoon.teamcat.agent.debug;

import org.apache.log4j.Level;
import org.apache.log4j.PatternLayout;
import org.junit.Test;

import com.xracoon.teamcat.agent.config.TeamcatAppender;

public class DebugDoraAppenderTestCase {

	@Test
	public void testDoraLog(){
		org.apache.log4j.Logger logger=org.apache.log4j.Logger.getLogger("logger4tq."+1);
		logger.setAdditivity(false);
		logger.setLevel(Level.INFO);
		PatternLayout layout = new PatternLayout("[%d - %t - %6p] %m%n");
		TeamcatAppender doraAppender = new TeamcatAppender(1l);
		doraAppender.setLayout(layout);
		logger.addAppender(doraAppender);
		for (int i = 0; i < 10; i++) {
	
			logger.info("Ignoring bean creation exception on FactoryBean type check: org.springframework.beans.factory.UnsatisfiedDependencyException: Error creating bean with name 'heroSkillDota2Mapper' defined in file [/web/resin_vhost/cdss.766.com/WEB-INF/classes/com/carry6/cdss/mapper/dota2/HeroSkillDota2Mapper.class]: Unsatisfied dependency expressed through bean property 'sqlSessionFactory': : Error creating bean with name 'compEventDota2Mapper' defined in file [/web/resin_vhost/cdss.766.com/WEB-INF/classes/com/carry6/cdss/mapper/dota2/CompEventDota2Mapper.class]: Instantiation of bean failed; nested exception is java.lang.StackOverflowError; nested exception is org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'compEventDota2Mapper' defined in file [/web/resin_vhost/cdss.766.com/WEB-INF/classes/com/carry6/cdss/mapper/dota2/CompEventDota2Mapper.class]: Instantiation of bean failed; nested exception is java.lang.StackOverflowError"+i);
			try {
				Thread.sleep(100000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}
}
