package pl.simpatico.pgrexample.client;

import pl.simpatico.pgrexample.client.services.*;
import pl.simpatico.pgrexample.client.vo.ExampleVo2;
import pl.simpatico.pgrexample.client.vo.ExampleVo3;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.rpc.ServiceDefTarget;
import com.google.gwt.user.client.ui.*;

public class PgrExample implements EntryPoint {


    public void onModuleLoad() {
        final ExampleServiceAsync ourInstance = (ExampleServiceAsync)
                GWT.create(ExampleService.class);
        
        ((ServiceDefTarget) ourInstance).setServiceEntryPoint("/services");

        Button bt1 = new Button("test1");
        RootPanel.get().add(bt1);
        bt1.addClickListener(new ClickListener() {
            public void onClick(Widget arg0) {
                log("Try to add two int values 5 + 3:");
                ourInstance.sumInts(5, 3, callback);
            }
        });

        Button bt2 = new Button("test2 (user role)");
        RootPanel.get().add(bt2);
        bt2.addClickListener(new ClickListener() {
            public void onClick(Widget arg0) {
                log("Try to cut array ['a','b','c','d'] from 2 to 4");
                ourInstance.subArray(new String[]{"a", "b", "c", "d"}, 2, 4, callback);
            }
        });

        Button bt3 = new Button("test3 (adm role)");
        RootPanel.get().add(bt3);
        bt3.addClickListener(new ClickListener() {
            public void onClick(Widget arg0) {
                log("Try to read sub object and rewrite values");
                ExampleVo2 vo = new ExampleVo2();
                vo.setIntField(1);
                vo.setStrField("wedad");
                ExampleVo3 vo1 = new ExampleVo3();
                vo1.setIntField(11);
                vo1.setStrField("dsd");
                vo.setObjField(vo1);
                ourInstance.subObject(vo, callback);
            }
        });

        Button bt4 = new Button("login as user");
        RootPanel.get().add(bt4);
        bt4.addClickListener(new ClickListener() {
            public void onClick(Widget arg0) {
                log("Try to login with 'user' role");
                ourInstance.loginUser("user","pass", callback);
            }
        });

        Button bt5 = new Button("login as mgr");
        RootPanel.get().add(bt5);
        bt5.addClickListener(new ClickListener() {
            public void onClick(Widget arg0) {
                log("Try to login with 'mgr' role");
                ourInstance.loginUser("mgr","pass", callback);
            }
        });

        Button bt6 = new Button("login as adm");
        RootPanel.get().add(bt6);
        bt6.addClickListener(new ClickListener() {
            public void onClick(Widget arg0) {
                log("Try to login with 'adm' role");
                ourInstance.loginUser("adm","pass", callback);
            }
        });

        Button bt7 = new Button("logout");
        RootPanel.get().add(bt7);
        bt7.addClickListener(new ClickListener() {
            public void onClick(Widget arg0) {
                log("Try to logout");
                ourInstance.logout(callback);
            }
        });

    }

    private void log(String s) {
        RootPanel.get().add(new Label(s));
    }


    private AsyncCallback callback = new AsyncCallback() {
        public void onFailure(Throwable arg0) {
            log("---> error : " + arg0.getMessage());
        }

        public void onSuccess(Object arg0) {
            if (arg0 instanceof Object[]) {
                Object[] ob = (Object[]) arg0;
                String s = "[";
                for (int i = 0; i < ob.length; i++) {
                    s = s + "'" + ob[i] + "'";
                }
                s = s + "]";
                log("---> success : " + s);
            } else {
                log("---> success : " + arg0);
            }

        }
    };
}
