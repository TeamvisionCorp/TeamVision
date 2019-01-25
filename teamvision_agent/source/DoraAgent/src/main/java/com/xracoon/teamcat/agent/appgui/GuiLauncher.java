package com.xracoon.teamcat.agent.appgui;

import java.awt.EventQueue;

/**
 * Agent GUI启动类
 * @author Yangtianxin
 */
public class GuiLauncher {
	public static void main(String[] args)
	{
		EventQueue.invokeLater(new Runnable(){
			@Override
			public void run() {
				MainFrame frame=new MainFrame();
				frame.setVisible(true);
			}});
	}
}
