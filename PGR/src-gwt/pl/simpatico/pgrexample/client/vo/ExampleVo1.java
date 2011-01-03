package pl.simpatico.pgrexample.client.vo;

import java.io.Serializable;
import java.util.List;

public class ExampleVo1 implements Serializable{

    private String strField;
	private int intField;
	
	public void setStrField(String strField) {
		this.strField = strField;
	}
	public String getStrField() {
		return strField;
	}
	public void setIntField(int intField) {
		this.intField = intField;
	}
	public int getIntField() {
		return intField;
	}
	
	public String toString() {
		return "ExampleVo1: {strField: '" +getStrField() + "', intField: " +getIntField() +"}";
	}

}
