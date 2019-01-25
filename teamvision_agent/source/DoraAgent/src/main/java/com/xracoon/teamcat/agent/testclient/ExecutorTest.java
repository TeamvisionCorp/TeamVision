package com.xracoon.teamcat.agent.testclient;

public class ExecutorTest {
	public static void main(String[] args)
	{
//		ExecutorService service=Executors.newSingleThreadExecutor();
//		service.submit(new Runnable(){
//			@Override
//			public void run() {
//				int i=0;
//				while(true)
//				{
//					System.out.println(i);
//				}
//			}});
		
		Thread testThread=new Thread(new Runnable(){
			@Override
			public void run() {
				int i=0;
				while(true)
				{
					System.out.println(i++);
				}
			}
		});
		testThread.start();
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		testThread.stop();
	}
}
