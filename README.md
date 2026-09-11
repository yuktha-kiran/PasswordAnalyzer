# 🔐 AI-Based Password Security Analyzer

A web-based **Application Security** project that analyzes password characteristics and provides an intelligent password security assessment using Machine Learning.

> **Academic Project:** CSE535 — Cryptography & Network Security  
> **Focus Area:** U5 — Application Security  
> **Project Type:** CIA-3 Component 2 — Micro Project

---

## 📌 Project Overview

Weak and predictable passwords are a major concern in application security.

The **AI-Based Password Security Analyzer** helps users understand the security characteristics of a password. The system extracts multiple password features and uses a **Random Forest Machine Learning classifier** to classify the password as Weak, Medium, or Strong.

The application also provides a security score, risk assessment, detected weaknesses, and recommendations for improving password security.

---

## 🎯 Problem Statement

Many users create passwords using predictable patterns, short words, repeated characters, or common sequences. Such passwords can increase the risk of unauthorized access.

Traditional password checkers often rely only on fixed rules. This project develops a Machine Learning-based password-security analyzer that uses multiple password characteristics to classify password strength.

---

## 🎯 Objectives

- Develop a web-based password security analyzer.
- Analyze important password characteristics.
- Identify weak and predictable password patterns.
- Classify passwords into security levels.
- Calculate a user-friendly security score.
- Provide meaningful security recommendations.
- Implement a Machine Learning-based password classification system.
- Demonstrate an Application Security use case using AI/ML.

---

## ✨ Key Features

### 🔐 Password Analysis

The system analyzes characteristics such as:

- Password length
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters
- Unique characters
- Repeated characters
- Predictable sequences
- Common password patterns
- Estimated character entropy

### 🤖 AI/ML-Based Classification

A **Random Forest Classifier** is used to classify passwords into three categories:

- 🔴 **Weak**
- 🟠 **Medium**
- 🟢 **Strong**

The model uses **14 extracted features** from each password.

### 📊 Security Score

The application provides a user-friendly security score from **0 to 100**.

```text
0 ─────────────────────────────── 100
Low Security                  High Security