#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
from sklearn.metrics import roc_curve, auc, average_precision_score, precision_recall_curve

from lib.base_classes.object_base import ObjectBase
from lib.testable.reporter_component import ReportComponent
from lib.testable.pdf_generator import PdfGenerator

class ReporterBase(ObjectBase):

    def __init__(self, name='', defaults={}, **kwargs):
        """
        Initialize report utility object.
        @param analysis_dict: Analysis plan specified as a dictionary with function name (strings) as keys and list of
        variable names to apply for each as values. The variable names are prefixes in the standard results dataframe.
        """
        ObjectBase.__init__(self, name, defaults, **kwargs)
        self.report_df = None
        self.pdf_generator = PdfGenerator()
        self.analysis_dict = {}
        self.image_dir = ''
        self.init_report_dirs()
        self.init_analysis_dict()

    def __call__(self, df , report_path='', report_header=''):
        """
        Generate report component list for a results standard dataframe.
        @param df: results standard dataframe with: pred, prob, target, tp, fn ,fp, and tn per variable.
        @return: List of report components generated according to the analysis plan in the analysis dictionary.
        """
        report_path   = self.get_report_path(report_path)
        report_header = self.get_report_header(report_header)
        df.to_csv(os.path.join(report_path, 'df.csv'))
        return self.generate_report(df, report_path, report_header)

    def get_report_path(self, path = ''):
        return path
    
    def get_report_header(self, header = ''):
        return header

    def generate_report(self, df, report_path='', report_header=''):
        report_component_list = self.get_componenets_list(df)
        self.pdf_generator(report_component_list, report_path, report_header)

    def get_componenets_list(self, df):
        self.report_df = df
        report_component_list = []
        for key, val in self.analysis_dict.items():
            report_component_list.extend(getattr(self, key)(df, val))
        return report_component_list

    def init_image_dir(self, path=''):
        self.image_dir = path
    
    def init_analysis_dict(self):
        self.analysis_dict = {}

    @staticmethod
    def get_per_var_df(df, var):
        """
        Get variable dataframe with counts and proportions of confusion matrix cases: tp, fn, fp, tn.
        @param df: results standard dataframe with: pred, prob, target, tp, fn ,fp, and tn per variable.
        @param var: variable name to get results for
        @return: dataframe with 4 rows (one per case) and 2 columns: n and proportion
        """
        col_order = ['tp', 'fn', 'fp', 'tn']
        col_names = [f'{var}_{col}' for col in col_order]
        var_df = pd.DataFrame(df[col_names].sum(), columns=['n'])
        divider =  var_df['n'].sum() if  var_df['n'].sum()>0 else 1
        var_df['ratio'] = var_df['n'] / divider
        var_df.index = col_order
        return var_df

    def plot_confusion_matrix(self, ratio_mat, n_mat, col_order_mat, var_name):
        """
        Produce confusion matrix plot and save as png in the images directory.
        @param ratio_mat: matrix of ratio for each result (tp, fn , fp, fn) as 2*2 matrix, respectively.
        @param n_mat: matrix of count for each result (tp, fn , fp, fn) as 2*2 matrix
        @param col_order_mat: matrix of result case name (tp, fn , fp, fn) as 2*2 matrix
        @param var_name: variable name to plot
        @return: image path for saved figure
        """
        plt.imshow(ratio_mat, vmin=0., vmax=1., cmap='Blues')
        plt.xticks(np.arange(2), ['target', 'non target'])
        plt.yticks(np.arange(2), ['target', 'non target'], rotation=90, va='center')
        plt.colorbar()
        plt.ylabel('true label')
        plt.xlabel('predicted label')
        for i in range(ratio_mat.shape[0]):
            for j in range(ratio_mat.shape[1]):
                res_str = f'{col_order_mat[i, j]}\n{ratio_mat[i, j]:.2f} ({n_mat[i, j]})'
                plt.text(j, i, res_str, ha='center')
        im_path = os.path.join(self.image_dir, f'{var_name}_cm.png')
        plt.savefig(im_path)
        plt.close()
        return im_path

    # def intersection_over_union(self, df, var_l):
    #     def parse(s):
    #         if s is np.nan:
    #             return s
    #
    #         for char in string.punctuation:
    #             s = s.replace(char, ' ')
    #
    #         return " ".join(s.split()).lower().strip()
    #
    #     def iou(row):
    #         target_val = [row[0]]
    #         pred_val = [row[1]]
    #
    #         union = target_val.copy()
    #         intersection = []
    #         for t in pred_val:
    #             if t in target_val:
    #                 target_val.remove(t)
    #                 intersection.append(t)
    #             else:
    #                 union.append(t)
    #
    #         return len(intersection) / float(len(union))
    #
    #     def calc_iou(target_val, pred_val):
    #         target_val.apply(lambda x: [parse(y) for y in x.split()])
    #         pred_val.apply(lambda x: [parse(y) for y in x.split()])
    #
    #         target_val_df = pd.DataFrame(target_val)
    #         pred_val_df = pd.DataFrame(pred_val)
    #         concate = pd.concat([target_val_df, pred_val_df], axis=1, sort=False)
    #         return concate.apply(iou, axis=1)
    #
    #
    #     text = ''
    #     for var in var_l:
    #         var_df_pred = df[f'{var}_pred']
    #         var_df_pre_forcer_pred = df[f'{var}_pre_forcer']
    #         var_df_target = df[f'{var}_target']
    #
    #         IOU_df = calc_iou(var_df_target, var_df_pred)
    #         IOU_pre_forcer_df = calc_iou(var_df_target, var_df_pre_forcer_pred)
    #
    #         text += f'\n{var}_avg_IOU: {np.average(IOU_df)}'
    #         text += f'\n{var}_avg_IOU_pre_forcer: {np.average(IOU_pre_forcer_df)}\n'
    #     component = ReportComponent(pre_text=text)
    #
    #     return [component]

    def confusion_matrix(self, df, var_l):
        """
        Create confusion matrix report components per variable in variable list. Each would have its own component.
        @param df: Results standard dataframe with: pred, prob, target, tp, fn ,fp, and tn per variable.
        @param var_l: variable name list (prefixes in df)
        @return: component list
        """
        component_l = []
        for var in var_l:
            var_df = self.get_per_var_df(df, var)
            ratio_mat = var_df.ratio.values.reshape(2, 2)
            n_mat = var_df.n.values.reshape(2, 2)
            col_order_mat = np.array(var_df.index).reshape(2, 2)
            image_path = self.plot_confusion_matrix(ratio_mat, n_mat, col_order_mat, var)
            f1, precision, recall = self.calculate_f1_precision_recall(var_df.loc['tp'].n, var_df.loc['fn'].n,
                                                                       var_df.loc['fp'].n)
            title = f'confusion matrix {var}'
            pre_text = f''
            post_text = f'F1={f1:.2f}\tprecision={precision:.2f}\trecall={recall:.2f}'
            component = ReportComponent(title, pre_text, [image_path], post_text)
            component_l.append(component)
        return component_l

    def plot_f1_precision_recall(self, plot_df):
        """
        Plot and save figure for f1 precision recall bar plot per variable.
        @param plot_df: Aggregated dataframe indexed by variable names and with f1, precision and recall for each.
        @return: image path.
        """
        plot_df.plot.bar()
        im_path = os.path.join(self.image_dir, 'f1_precision_recall.png')
        plt.tight_layout()
        plt.savefig(im_path)
        plt.close()
        return im_path

    def f1_precision_recall(self, df, var_l):
        """
        Create f1, precision and recall comparison component for the variable list.
        @param df: Results standard dataframe with: pred, prob, target, tp, fn ,fp, and tn per variable.
        @param var_l: Variable list to compare (may also be a single variable)
        @return: Component list (with single component)
        """
        plot_df = pd.DataFrame(index=var_l, columns=['f1', 'precision', 'recall'])
        for var in var_l:
            var_df = self.get_per_var_df(df, var)
            f1, precision, recall = self.calculate_f1_precision_recall(var_df.loc['tp'].n, var_df.loc['fn'].n,
                                                                       var_df.loc['fp'].n)
            plot_df.loc[var] = [f1, precision, recall]
        image_path = self.plot_f1_precision_recall(plot_df)
        title = f'overall performance'
        pre_text = f''
        post_text = f''
        component = ReportComponent(title, pre_text, [image_path], post_text)
        return [component]

    @staticmethod
    def calculate_f1_precision_recall(tp, fn, fp):
        """
        Calculate f1, precision and recall given count of tp, fn and fp.
        @param tp: true positive count
        @param fn: false negative count
        @param fp: false positive count
        @return: f1, precision and recall
        """
        if tp + fp == 0:
            recall = 0
            precision = 0
            f1 = 0
        else:
            tp_and_fn = (tp + fn) if (tp + fn) else 1
            tp_and_fp = (tp + fp) if (tp + fp) else 1
            recall = tp / tp_and_fn
            precision = tp / tp_and_fp
            if recall + precision == 0:
                divider = 1
            else:
                divider = (precision + recall)
            f1 = 2 * precision * recall / divider
        return f1, precision, recall

    def plot_roc_auc(self, fpr, tpr, var):
        """
        Plot a receiver operating characteristic curve and save image as png.
        @param fpr: false positive rate vector
        @param tpr: true positive rate vector
        @param var: variable name
        @return: image path.
        """
        plt.plot(fpr, tpr)
        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.legend(loc="lower right")
        im_path = os.path.join(self.image_dir, f'{var}_roc_auc.png')
        plt.savefig(im_path)
        plt.close()
        return im_path

    def roc_auc(self, df, var_l):
        """
        Create ROC component per variable in variable list.
        @param df: Results standard dataframe with: pred, prob, target, tp, fn ,fp, and tn per variable.
        @param var_l: List of variable names to get ROCs for.
        @return: List of ROC components per variable.
        """
        component_l = []
        for var in var_l:
            prediction_vec = df[f'{var}_prob']
            target_vec = np.logical_or(df[f'{var}_tp'], df[f'{var}_fn'])
            fpr, tpr, _ = roc_curve(target_vec, prediction_vec)
            auc_score = auc(fpr, tpr)
            image_path = self.plot_roc_auc(fpr, tpr, var)
            title = f'{var} receiver operating characteristic'
            pre_text = f''
            post_text = f'AUC = {auc_score:.2f}'
            component = ReportComponent(title, pre_text, [image_path], post_text)
            component_l.append(component)
        return component_l

    def plot_precision_recall_curve(self, precision, recall, var):
        """
        Plot precision recall curve and save figure as png.
        @param precision: Precision vector.
        @param recall: Recall vector.
        @param var: Variable name.
        @return: Image path.
        """
        plt.step(recall, precision, where='post')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        im_path = os.path.join(self.image_dir, f'{var}_precision_recall_curve.png')
        plt.savefig(im_path)
        plt.close()
        return im_path

    def precision_recall_curve(self, df, var_l):
        """
        Create precision recall curve component per variable in variable list.
        @param df: Results standard dataframe with: pred, prob, target, tp, fn ,fp, and tn per variable.
        @param var_l: Variable list to generate precision recall curve for.
        @return: List of report components.
        """
        component_l = []
        for var in var_l:
            prediction_vec = df[f'{var}_prob']
            target_vec = np.logical_or(df[f'{var}_tp'], df[f'{var}_fn'])
            precision, recall, _ = precision_recall_curve(target_vec, prediction_vec)
            average_precision = average_precision_score(target_vec, prediction_vec)
            image_path = self.plot_precision_recall_curve(precision, recall, var)
            title = f'{var} precision recall curve'
            pre_text = f''
            post_text = f'AP = {average_precision:.2f}'
            component = ReportComponent(title, pre_text, [image_path], post_text)
            component_l.append(component)
        return component_l
