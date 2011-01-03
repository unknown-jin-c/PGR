package pl.simpatico.pgrexample.client.vo;

import java.io.Serializable;

public class ExampleVo3 implements Serializable{
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
		return "ExampleVo3: {strField: '" +strField + "', intField: " +intField +"}";
	}
}
