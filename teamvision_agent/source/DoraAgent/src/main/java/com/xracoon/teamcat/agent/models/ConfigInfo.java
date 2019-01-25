package com.xracoon.teamcat.agent.models;


public class ConfigInfo {
    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getDicDataName() {
        return DicDataName;
    }

    public void setDicDataName(String dicDataName) {
        DicDataName = dicDataName;
    }

    public Integer getDicDataValue() {
        return DicDataValue;
    }

    public void setDicDataValue(Integer dicDataValue) {
        DicDataValue = dicDataValue;
    }

    public String getDicDataDesc() {
        return DicDataDesc;
    }

    public void setDicDataDesc(String dicDataDesc) {
        DicDataDesc = dicDataDesc;
    }

    public Boolean getDicDataIsActive() {
        return DicDataIsActive;
    }

    public void setDicDataIsActive(Boolean dicDataIsActive) {
        DicDataIsActive = dicDataIsActive;
    }

    public Integer getDicType() {
        return DicType;
    }

    public void setDicType(Integer dicType) {
        DicType = dicType;
    }

    private Integer id;
    private String DicDataName;
    private Integer DicDataValue;
    private String DicDataDesc;
    private Boolean DicDataIsActive;
    private Integer DicType;
}
