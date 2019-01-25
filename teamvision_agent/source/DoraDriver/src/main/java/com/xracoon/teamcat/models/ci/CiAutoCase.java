package com.xracoon.teamcat.models.ci;

public class CiAutoCase {
    private Integer id;
    private Boolean IsActive;

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Boolean getActive() {
        return IsActive;
    }

    public void setActive(Boolean active) {
        IsActive = active;
    }

    public String getPackageName() {
        return PackageName;
    }

    public void setPackageName(String packageName) {
        PackageName = packageName;
    }

    public String getClassName() {
        return ClassName;
    }

    public void setClassName(String className) {
        ClassName = className;
    }

    public String getCaseName() {
        return CaseName;
    }

    public void setCaseName(String caseName) {
        CaseName = caseName;
    }

    public Integer getCaseType() {
        return CaseType;
    }

    public void setCaseType(Integer caseType) {
        CaseType = caseType;
    }

    public Integer getProjectID() {
        return ProjectID;
    }

    public void setProjectID(Integer projectID) {
        ProjectID = projectID;
    }

    public Integer getModuleID() {
        return ModuleID;
    }

    public void setModuleID(Integer moduleID) {
        ModuleID = moduleID;
    }

    public Integer getInterfaceID() {
        return InterfaceID;
    }

    public void setInterfaceID(Integer interfaceID) {
        InterfaceID = interfaceID;
    }

    public String getCaseTag() {
        return CaseTag;
    }

    public void setCaseTag(String caseTag) {
        CaseTag = caseTag;
    }

    public Integer getVersion() {
        return Version;
    }

    public void setVersion(Integer version) {
        Version = version;
    }

    public String getDesc() {
        return Desc;
    }

    public void setDesc(String desc) {
        Desc = desc;
    }

    private String PackageName;
    private String ClassName;
    private String CaseName;
    private Integer CaseType;
    private Integer ProjectID;
    private Integer ModuleID;
    private Integer InterfaceID;
    private String CaseTag;
    private Integer Version;
    private String Desc;
}
