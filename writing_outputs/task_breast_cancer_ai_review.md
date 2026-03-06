# 任务：乳腺癌AI诊断研究进展综述

## 目标
写一篇中文学术综述论文，主题：人工智能在乳腺癌诊断中的研究进展。

## 要求
- **语言**：中文正文，英文引用
- **引用格式**：APA 7th edition，BibTeX 管理
- **输出格式**：LaTeX → PDF
- **结构**：综述论文结构（不是 IMRaD，是综述的 Introduction → 主题分类 → Discussion → Conclusion）

## 内容大纲
1. 引言：乳腺癌流行病学背景、AI 在医学影像中的兴起
2. AI 在乳腺X线摄影（Mammography）中的应用
   - CNN 架构（ResNet, DenseNet, EfficientNet 等）
   - 商业 AI 系统（Lunit INSIGHT, Transpara 等）
   - 临床试验结果
3. AI 在乳腺超声诊断中的应用
4. AI 在乳腺 MRI 中的应用
5. AI 在组织病理学图像分析中的应用
   - 全切片图像（WSI）分析
   - HER2/Ki-67 等生物标志物预测
6. 多模态融合与可解释性 AI（XAI）
7. 挑战与展望
   - 数据隐私与联邦学习
   - 模型泛化与外部验证
   - 临床落地障碍
8. 结论

## 关键参考文献（从 PubMed 检索，必须使用这些真实文献）

1. Jiang B, et al. (2024). Deep learning applications in breast cancer histopathological imaging: diagnosis, treatment, and prognosis. Breast Cancer Res, 26(1):137. PMID: 39304962
2. Qi YJ, et al. (2024). Radiomics in breast cancer: Current advances and future directions. Cell Rep Med, 5(9):101719. PMID: 39293402
3. Zhang J, et al. (2023). Recent advancements in artificial intelligence for breast cancer: Image augmentation, segmentation, diagnosis, and prognosis approaches. Semin Cancer Biol, 96:11-25. PMID: 37704183
4. Díaz O, et al. (2024). Artificial Intelligence for breast cancer detection: Technology, challenges, and prospects. Eur J Radiol, 175:111457. PMID: 38640824
5. Al-Karawi D, et al. (2024). A Review of Artificial Intelligence in Breast Imaging. Tomography, 10(5):705-726. PMID: 38787015
6. Arun Kumar S, Sasikala S. (2023). Review on Deep Learning-Based CAD Systems for Breast Cancer Diagnosis. Technol Cancer Res Treat, 22:15330338231177977. PMID: 37282580
7. Abdullah KA, et al. (2025). Deep learning-based breast cancer diagnosis in breast MRI: systematic review and meta-analysis. Eur Radiol, 35(8):4474-4489. PMID: 39907762
8. Nasser M, Yusof UK. (2023). Deep Learning Based Methods for Breast Cancer Diagnosis: A Systematic Review and Future Direction. Diagnostics, 13(1):161. PMID: 36611453
9. Al Muhaisen S, et al. (2024). Artificial Intelligence-Powered Mammography: Navigating the Landscape of Deep Learning for Breast Cancer Detection. Cureus, 16(3):e56945. PMID: 38665752
10. Adam R, et al. (2023). Deep learning applications to breast cancer detection by magnetic resonance imaging: a literature review. Breast Cancer Res, 25(1):87. PMID: 37488621
11. Lowry KP, Zuiderveld CC. (2024). Artificial Intelligence for Breast Cancer Risk Assessment. Radiol Clin North Am, 62(4):619-625. PMID: 38777538
12. Wang L. (2024). Mammography with deep learning for breast cancer detection. Front Oncol, 14:1281922. PMID: 38410114
13. Ghasemi A, et al. (2024). Explainable artificial intelligence in breast cancer detection and risk prediction: A systematic scoping review. Cancer Innov, 3(5):e136. PMID: 39430216
14. Priya CVL, et al. (2024). Deep learning approaches for breast cancer detection in histopathology images: A review. Cancer Biomark, 40(1):1-25. PMID: 38517775
15. Kinkar KK, et al. (2024). Empowering breast cancer diagnosis and radiology practice: advances in artificial intelligence for contrast-enhanced mammography. Front Radiol, 3:1326831. PMID: 38249158

## 额外要求
- 还需补充更多经典文献（如 McKinney et al. 2020 Nature; Shen et al. 2019 Sci Rep; Bejnordi et al. 2017 JAMA 等里程碑论文）
- 每个主题章节至少引用 5-8 篇文献
- 总引用量目标：40-60 篇
- 写完后编译为 PDF

## 输出目录
writing_outputs/20260305_breast_cancer_ai_review/
- drafts/v1_draft.tex
- references/references.bib
- figures/ (如果生成了图)
- final/manuscript.pdf

## 注意
- 正文用中文，参考文献用英文
- 使用 ctex 宏包处理中文
- 不要用 bullet points，全部用流畅的段落式学术写作
- 编译命令：xelatex → bibtex → xelatex × 2
