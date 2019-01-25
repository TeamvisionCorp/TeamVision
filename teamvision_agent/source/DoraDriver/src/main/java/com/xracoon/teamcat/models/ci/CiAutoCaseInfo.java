package com.xracoon.teamcat.models.ci;

import java.util.List;

public class CiAutoCaseInfo {
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

    public CiAutoCases getResult() {
        return result;
    }

    public void setResult(CiAutoCases result) {
        this.result = result;
    }

    private Integer code;
    private String message;
    private CiAutoCases result;

    public class CiAutoCases{
        private Integer count;
        private String next;
        private String previous;

        public Integer getCount() {
            return count;
        }

        public void setCount(Integer count) {
            this.count = count;
        }

        public String getNext() {
            return next;
        }

        public void setNext(String next) {
            this.next = next;
        }

        public String getPrevious() {
            return previous;
        }

        public void setPrevious(String previous) {
            this.previous = previous;
        }

        public List<CiAutoCase> getResults() {
            return results;
        }

        public void setResults(List<CiAutoCase> results) {
            this.results = results;
        }

        private List<CiAutoCase> results;
    }
}
