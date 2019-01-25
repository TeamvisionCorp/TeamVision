package com.xracoon.teamcat.agent.models;

import java.util.List;

public class DicConfigs {
    private Integer code;

    public Integer getCode() {
        return code;
    }

    public void setCode(Integer code) {
        this.code = code;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public List<ConfigInfo> getResult() {
        return result;
    }

    public void setResult(List<ConfigInfo> result) {
        this.result = result;
    }

    private String message;
    private List<ConfigInfo> result;
}
