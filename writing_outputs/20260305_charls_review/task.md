# 任务：CHARLS数据库研究进展综述（图文并茂）

## 目标
写一篇中文学术综述论文，主题：中国健康与养老追踪调查（CHARLS）数据库的研究进展与应用。
要求图文并茂，需要生成专业的科学示意图。

## 背景
CHARLS（China Health and Retirement Longitudinal Study）是由北京大学国家发展研究院主持的大规模纵向追踪调查，参照美国HRS（Health and Retirement Study）设计，覆盖全国28个省份约2万名45岁以上中老年人。自2011年全国基线调查以来，已完成多轮追踪（2013、2015、2018、2020），积累了丰富的健康、经济、社会数据。

## 文献来源
- `sources/all_abstracts.txt` 包含74篇从PubMed检索到的CHARLS相关论文完整摘要
- 你必须基于这些真实文献来写，引用必须是真实的
- 可以补充其他你知道的经典CHARLS文献（如Zhao et al. 2014 cohort profile等）

## 内容大纲
1. 引言：中国老龄化背景、CHARLS数据库的创建与意义
2. CHARLS数据库概述：设计、抽样、数据波次、核心模块
3. 心血管疾病与代谢健康研究
4. 认知功能衰退与痴呆研究
5. 抑郁与心理健康研究
6. 衰弱、肌少症与身体功能研究
7. 环境与社会因素健康效应
8. 方法学创新（机器学习、因果推断等）
9. 局限性与未来展望
10. 结论

## 图表要求（关键！）
本文必须包含至少4-5张专业图表。使用Python matplotlib/seaborn生成：

1. **CHARLS研究设计流程图** — 展示数据波次、样本量、核心模块
2. **研究主题分布图** — 饼图或柱状图，展示不同研究领域的论文数量
3. **主要发现汇总表** — 关键研究的OR/HR值森林图风格展示
4. **CHARLS与国际队列对比表** — 与HRS、ELSA、SHARE等的对比
5. **研究趋势时间线** — 按年份展示CHARLS论文发表趋势

图表规范：
- 使用中文标签
- 绘图前检测CJK字体：运行 `python3 skills/cjk-viz/scripts/setup_cjk_font.py`，使用返回的字体
- matplotlib backend 使用 Agg
- 保存为PNG，300dpi
- 保存到 writing_outputs/20260305_charls_review/figures/ 目录

## 格式要求
- 语言：中文正文，英文引用
- 引用格式：APA 7th，BibTeX管理
- 输出：LaTeX (ctex + xelatex) → PDF
- 全部用流畅段落式写作，不用bullet points
- 编译命令：xelatex → bibtex → xelatex × 2

## 输出
- drafts/v1_draft.tex
- references/references.bib
- figures/*.png（至少4-5张）
- final/manuscript.pdf

## 完成后
运行: openclaw system event --text "Done: CHARLS综述完成，含图表" --mode now
