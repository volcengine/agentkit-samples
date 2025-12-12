"use strict";

module.exports = {
  names: ["required-headers"],
  description: "Ensure README contains specific required headers",
  tags: ["structure"],

  function: function rule(params, onError) {
    const requiredHeaders = [
      "# 项目介绍",
      "## 安装",
      "## 使用方法",
      "## 运行结果"
    ];

    const content = params.lines.join("\n");

    requiredHeaders.forEach((header) => {
      if (!content.includes(header)) {
        onError({
          lineNumber: 1,
          detail: `Missing required header: "${header}"`
        });
      }
    });
  }
};