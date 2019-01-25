package com.xracoon.teamcat.agent.appgui;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.Label;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.DefaultListModel;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JList;

public class MainFrame extends JFrame{
	private static final long serialVersionUID = -3924567186310587858L;

	public MainFrame()
	{
		setTitle("Teamcat Agent");
		setSize(800, 600);
		setLocationRelativeTo(null);  //居中，setLocationRelativeTo()方法一定要JDialog的SetSize()方法的后面，否则窗体的左上角会出屏幕或者所属组件的中心，即窗体实际上的位置看起来是偏向右下角的
		setDefaultCloseOperation(EXIT_ON_CLOSE); //0 DO_NOTHING_ON_CLOSE,1 HIDE_ON_CLOSE(default),2 DISPOSE_ON_CLOSE, 3 EXIT_ON_CLOSE(调用System.exit)
		setExtendedState(JFrame.MAXIMIZED_BOTH); 
		getContentPane().setLayout(new BorderLayout(0, 0));
		
		addWindowListener(new WindowAdapter(){
			@Override
			public void windowClosing(final WindowEvent event)
			{
				//logcatReader.stop();
			}
		});
		
		buildUI();
	}
	
	public void buildUI()
	{
		JPanel toolbar = new JPanel();
		getContentPane().add(toolbar, BorderLayout.NORTH);
		toolbar.setSize(200, 100);
		toolbar.setLayout(new FlowLayout());
		
		Label label=new Label("Agent");
		toolbar.add(label);
		
		DefaultListModel<String> listModel = new DefaultListModel<>();
	    listModel.addElement("Debbie Scott");
	    listModel.addElement("Scott Hommel");
	    listModel.addElement("Sharon Zakhour");
	    
		JList<String> list = new JList<String>(listModel);
		getContentPane().add(list, BorderLayout.WEST);

	}
	
}
