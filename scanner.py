"""
主扫描器模块 - 整合所有功能
"""
from datetime import datetime
from typing import List, Dict, Optional
from github_scanner import GitHubScanner
from secret_detector import SecretDetector
from report_generator import ReportGenerator
from scan_history import ScanHistory


class CloudScanner:
    """云上扫描器 - 主要扫描逻辑"""
    
    def __init__(self, github_token: str, skip_scanned: bool = True):
        """
        初始化扫描器
        
        Args:
            github_token: GitHub Personal Access Token
            skip_scanned: 是否跳过已扫描的仓库 (默认: True)
        """
        self.github_scanner = GitHubScanner(github_token)
        self.secret_detector = SecretDetector()
        self.report_generator = ReportGenerator()
        self.scan_history = ScanHistory()
        self.skip_scanned = skip_scanned
    
    def scan_user(self, username: str) -> str:
        """
        扫描指定用户的所有公开仓库
        
        Args:
            username: GitHub用户名
            
        Returns:
            报告文件路径
        """
        print(f"🚀 开始扫描用户: {username}")
        scan_start_time = datetime.now()
        
        # 获取用户的所有仓库
        repos = self.github_scanner.get_user_repos(username)
        print(f"📦 找到 {len(repos)} 个公开仓库")
        
        # 过滤已扫描的仓库
        repos_to_scan, skipped_count = self._filter_scanned_repos(repos)
        if skipped_count > 0:
            print(f"⏭️  跳过 {skipped_count} 个已扫描的仓库")
            print(f"📦 需要扫描 {len(repos_to_scan)} 个新仓库")
        
        # 扫描所有仓库
        all_findings = []
        for idx, repo in enumerate(repos_to_scan, 1):
            print(f"🔍 [{idx}/{len(repos_to_scan)}] 扫描仓库: {repo['full_name']}")
            findings = self._scan_repository(repo, scan_type=f"user:{username}")
            all_findings.extend(findings)
        
        # 生成报告
        print(f"\n📝 生成报告...")
        report_path = self.report_generator.generate_report(
            all_findings, 
            scan_start_time,
            scan_type=f"user:{username}"
        )
        
        # 打印摘要
        summary = self.report_generator.generate_summary(report_path, len(all_findings))
        print(summary)
        
        return report_path
    
    def scan_organization(self, org_name: str) -> str:
        """
        扫描指定组织的所有公开仓库
        
        Args:
            org_name: GitHub组织名
            
        Returns:
            报告文件路径
        """
        print(f"🚀 开始扫描组织: {org_name}")
        scan_start_time = datetime.now()
        
        # 获取组织的所有仓库
        repos = self.github_scanner.get_org_repos(org_name)
        print(f"📦 找到 {len(repos)} 个公开仓库")
        
        # 过滤已扫描的仓库
        repos_to_scan, skipped_count = self._filter_scanned_repos(repos)
        if skipped_count > 0:
            print(f"⏭️  跳过 {skipped_count} 个已扫描的仓库")
            print(f"📦 需要扫描 {len(repos_to_scan)} 个新仓库")
        
        # 扫描所有仓库
        all_findings = []
        for idx, repo in enumerate(repos_to_scan, 1):
            print(f"🔍 [{idx}/{len(repos_to_scan)}] 扫描仓库: {repo['full_name']}")
            findings = self._scan_repository(repo, scan_type=f"org:{org_name}")
            all_findings.extend(findings)
        
        # 生成报告
        print(f"\n📝 生成报告...")
        report_path = self.report_generator.generate_report(
            all_findings,
            scan_start_time,
            scan_type=f"org:{org_name}"
        )
        
        # 打印摘要
        summary = self.report_generator.generate_summary(report_path, len(all_findings))
        print(summary)
        
        return report_path
    
    def scan_ai_projects(self, max_repos: int = 50) -> str:
        """
        自动搜索并扫描AI相关项目
        
        Args:
            max_repos: 最大扫描仓库数
            
        Returns:
            报告文件路径
        """
        print(f"🚀 开始自动搜索 AI 相关项目")
        scan_start_time = datetime.now()
        
        # 搜索AI相关仓库
        repos = self.github_scanner.search_ai_repos(max_repos=max_repos)
        print(f"📦 找到 {len(repos)} 个相关仓库")
        
        # 过滤已扫描的仓库
        repos_to_scan, skipped_count = self._filter_scanned_repos(repos)
        if skipped_count > 0:
            print(f"⏭️  跳过 {skipped_count} 个已扫描的仓库")
            print(f"📦 需要扫描 {len(repos_to_scan)} 个新仓库")
        
        # 扫描所有仓库
        all_findings = []
        for idx, repo in enumerate(repos_to_scan, 1):
            print(f"🔍 [{idx}/{len(repos_to_scan)}] 扫描仓库: {repo['full_name']}")
            findings = self._scan_repository(repo, scan_type="auto:ai-projects")
            all_findings.extend(findings)
        
        # 生成报告
        print(f"\n📝 生成报告...")
        report_path = self.report_generator.generate_report(
            all_findings,
            scan_start_time,
            scan_type="auto:ai-projects"
        )
        
        # 打印摘要
        summary = self.report_generator.generate_summary(report_path, len(all_findings))
        print(summary)
        
        return report_path
    
    def scan_single_repo(self, repo_full_name: str) -> str:
        """
        扫描单个仓库
        
        Args:
            repo_full_name: 仓库全名 (owner/repo)
            
        Returns:
            报告文件路径
        """
        print(f"🚀 开始扫描仓库: {repo_full_name}")
        scan_start_time = datetime.now()
        
        # 构建仓库信息
        repo_info = {
            'full_name': repo_full_name,
            'url': f"https://github.com/{repo_full_name}",
            'clone_url': f"https://github.com/{repo_full_name}.git",
        }
        
        # 扫描仓库
        findings = self._scan_repository(repo_info)
        
        # 生成报告
        print(f"\n📝 生成报告...")
        report_path = self.report_generator.generate_report(
            findings,
            scan_start_time,
            scan_type=f"single:{repo_full_name}"
        )
        
        # 打印摘要
        summary = self.report_generator.generate_summary(report_path, len(findings))
        print(summary)
        
        return report_path
    
    def _filter_scanned_repos(self, repos: List[Dict]) -> tuple:
        """
        过滤已扫描的仓库
        
        Args:
            repos: 仓库列表
            
        Returns:
            (需要扫描的仓库列表, 跳过的仓库数量)
        """
        if not self.skip_scanned:
            return repos, 0
        
        repos_to_scan = []
        skipped_count = 0
        
        for repo in repos:
            repo_name = repo.get('full_name', '')
            if self.scan_history.is_scanned(repo_name):
                skipped_count += 1
            else:
                repos_to_scan.append(repo)
        
        return repos_to_scan, skipped_count
    
    def _scan_repository(self, repo: Dict, scan_type: str = "unknown") -> List[Dict]:
        """
        扫描单个仓库
        
        Args:
            repo: 仓库信息字典
            scan_type: 扫描类型
            
        Returns:
            发现的敏感信息列表
        """
        findings = []
        scan_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        repo_name = repo.get('full_name', 'unknown')
        
        try:
            # 获取仓库文件列表
            files = self.github_scanner.get_repo_files(repo['full_name'])
            
            # 扫描每个文件
            for file_info in files:
                # 检查是否应该扫描该文件
                if not self.secret_detector.should_scan_file(file_info['path']):
                    continue
                
                # 获取文件内容
                content = self.github_scanner.get_file_content(
                    repo['full_name'],
                    file_info['path']
                )
                
                if content:
                    # 检测敏感信息
                    secrets = self.secret_detector.detect_secrets_in_text(
                        content,
                        file_info['path']
                    )
                    
                    # 添加仓库信息
                    for secret in secrets:
                        secret['repo_url'] = repo['url']
                        secret['repo_name'] = repo['full_name']
                        secret['scan_time'] = scan_time
                        findings.append(secret)
            
            # 去重和过滤
            findings = self.secret_detector.deduplicate_findings(findings)
            findings = self.secret_detector.filter_high_confidence(findings)
            
            if findings:
                print(f"  ⚠️  发现 {len(findings)} 个潜在问题")
            else:
                print(f"  ✅ 未发现明显问题")
            
            # 记录到扫描历史
            self.scan_history.mark_as_scanned(repo_name, len(findings), scan_type)
                
        except Exception as e:
            print(f"  ❌ 扫描失败: {e}")
            # 即使扫描失败，也记录以避免反复尝试
            self.scan_history.mark_as_scanned(repo_name, 0, f"{scan_type}:failed")
        
        return findings
