"""
报告生成模块
"""
import os
from datetime import datetime
from typing import List, Dict
from config import OUTPUT_DIR


class ReportGenerator:
    """扫描报告生成器"""
    
    def __init__(self, output_dir: str = OUTPUT_DIR):
        """
        初始化报告生成器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """确保输出目录存在"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_report(self, 
                       scan_results: List[Dict], 
                       scan_start_time: datetime,
                       scan_type: str = "auto") -> str:
        """
        生成扫描报告
        
        Args:
            scan_results: 扫描结果列表
            scan_start_time: 扫描开始时间
            scan_type: 扫描类型 (user/org/auto)
            
        Returns:
            报告文件路径
        """
        report_time = datetime.now()
        timestamp = report_time.strftime("%Y%m%d_%H%M%S")
        filename = f"scan_report_{timestamp}.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # 写入报告头
            f.write("=" * 60 + "\n")
            f.write("       InCloud GitHub 云上扫描器 - 扫描报告\n")
            f.write("=" * 60 + "\n\n")
            
            # 写入扫描信息
            f.write(f"扫描类型: {scan_type}\n")
            f.write(f"扫描开始时间: {scan_start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"报告生成时间: {report_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"发现的问题总数: {len(scan_results)}\n")
            f.write("\n" + "=" * 60 + "\n\n")
            
            # 如果没有发现问题
            if not scan_results:
                f.write("✅ 未发现敏感信息泄露！\n")
                f.write("\n扫描完成，一切正常。\n")
            else:
                # 按仓库分组
                results_by_repo = self._group_by_repo(scan_results)
                
                # 写入每个仓库的发现
                for repo_url, findings in results_by_repo.items():
                    self._write_repo_findings(f, repo_url, findings)
                
                # 写入统计信息
                self._write_statistics(f, scan_results)
            
            # 写入报告尾
            f.write("\n" + "=" * 60 + "\n")
            f.write("                    报告结束\n")
            f.write("=" * 60 + "\n")
        
        return filepath
    
    def _group_by_repo(self, scan_results: List[Dict]) -> Dict[str, List[Dict]]:
        """
        按仓库分组扫描结果
        
        Args:
            scan_results: 扫描结果列表
            
        Returns:
            按仓库分组的结果字典
        """
        grouped = {}
        for result in scan_results:
            repo_url = result.get('repo_url', 'Unknown')
            if repo_url not in grouped:
                grouped[repo_url] = []
            grouped[repo_url].append(result)
        return grouped
    
    def _write_repo_findings(self, f, repo_url: str, findings: List[Dict]):
        """
        写入单个仓库的发现
        
        Args:
            f: 文件对象
            repo_url: 仓库URL
            findings: 该仓库的发现列表
        """
        f.write("─" * 60 + "\n")
        f.write(f"🔍 仓库地址: {repo_url}\n")
        f.write(f"   发现问题数: {len(findings)}\n")
        f.write("─" * 60 + "\n\n")
        
        for idx, finding in enumerate(findings, 1):
            f.write(f"【问题 #{idx}】\n")
            
            # 网站地址（如果有）
            if finding.get('website'):
                f.write(f"  网站地址: {finding['website']}\n")
            
            # 文件信息
            f.write(f"  文件路径: {finding.get('file_path', 'N/A')}\n")
            
            # 行号
            if finding.get('line_number'):
                f.write(f"  行号: {finding['line_number']}\n")
            
            # 提交记录（如果有）
            if finding.get('commit_sha'):
                f.write(f"  提交记录: {finding['commit_sha']}\n")
            
            # 发现的密钥
            secret = finding.get('secret', '')
            # 部分隐藏密钥以保护安全
            masked_secret = self._mask_secret(secret)
            f.write(f"  发现的 API 密钥: {masked_secret}\n")
            
            # 置信度
            confidence = finding.get('confidence', 'unknown')
            confidence_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(confidence, '⚪')
            f.write(f"  置信度: {confidence_emoji} {confidence.upper()}\n")
            
            # 代码上下文
            if finding.get('line_content'):
                f.write(f"  代码片段: {finding['line_content'][:100]}\n")
            
            # 扫描时间
            if finding.get('scan_time'):
                f.write(f"  扫描时间: {finding['scan_time']}\n")
            
            f.write("\n")
        
        f.write("\n")
    
    def _mask_secret(self, secret: str) -> str:
        """
        部分隐藏密钥
        
        Args:
            secret: 原始密钥
            
        Returns:
            隐藏后的密钥
        """
        if len(secret) <= 8:
            return "*" * len(secret)
        
        # 显示前4个和后4个字符
        return f"{secret[:4]}{'*' * (len(secret) - 8)}{secret[-4:]}"
    
    def _write_statistics(self, f, scan_results: List[Dict]):
        """
        写入统计信息
        
        Args:
            f: 文件对象
            scan_results: 扫描结果列表
        """
        f.write("\n" + "=" * 60 + "\n")
        f.write("统计信息\n")
        f.write("=" * 60 + "\n\n")
        
        # 按置信度统计
        confidence_counts = {
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for result in scan_results:
            confidence = result.get('confidence', 'low')
            confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
        
        f.write(f"🔴 高置信度: {confidence_counts['high']} 个\n")
        f.write(f"🟡 中置信度: {confidence_counts['medium']} 个\n")
        f.write(f"🟢 低置信度: {confidence_counts['low']} 个\n")
        f.write(f"\n总计: {len(scan_results)} 个潜在问题\n\n")
        
        # 按仓库统计
        repos = set(r.get('repo_url') for r in scan_results)
        f.write(f"涉及仓库数: {len(repos)} 个\n\n")
        
        # 安全建议
        f.write("🛡️  安全建议:\n")
        f.write("  1. 立即轮换所有泄露的 API 密钥\n")
        f.write("  2. 使用环境变量或密钥管理服务存储敏感信息\n")
        f.write("  3. 在 .gitignore 中添加包含敏感信息的文件\n")
        f.write("  4. 使用 pre-commit hooks 防止敏感信息提交\n")
        f.write("  5. 定期审查代码仓库中的敏感信息\n")
    
    def generate_summary(self, report_path: str, total_findings: int) -> str:
        """
        生成简要摘要
        
        Args:
            report_path: 报告文件路径
            total_findings: 发现的问题总数
            
        Returns:
            摘要文本
        """
        summary = f"""
扫描完成！

报告已保存至: {report_path}
发现的潜在问题: {total_findings} 个

{"⚠️  建议立即检查报告并采取行动！" if total_findings > 0 else "✅ 未发现明显的敏感信息泄露。"}
"""
        return summary
