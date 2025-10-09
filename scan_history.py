"""
扫描历史管理模块 - 跟踪已扫描的仓库，避免重复扫描
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Set
from pathlib import Path


class ScanHistory:
    """扫描历史管理器"""
    
    def __init__(self, history_file: str = None):
        """
        初始化扫描历史管理器
        
        Args:
            history_file: 历史记录文件路径，默认为 scan_history/scanned_repos.json
        """
        if history_file is None:
            history_dir = Path("scan_history")
            history_dir.mkdir(exist_ok=True)
            self.history_file = history_dir / "scanned_repos.json"
        else:
            self.history_file = Path(history_file)
            self.history_file.parent.mkdir(exist_ok=True, parents=True)
        
        self.history = self._load_history()
    
    def _load_history(self) -> Dict:
        """
        从文件加载扫描历史
        
        Returns:
            历史记录字典
        """
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  加载扫描历史失败: {e}，将创建新历史记录")
                return {"repos": {}, "total_scanned": 0, "last_updated": None}
        else:
            return {"repos": {}, "total_scanned": 0, "last_updated": None}
    
    def _save_history(self):
        """保存扫描历史到文件"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  保存扫描历史失败: {e}")
    
    def is_scanned(self, repo_full_name: str) -> bool:
        """
        检查仓库是否已经被扫描过
        
        Args:
            repo_full_name: 仓库全名 (owner/repo)
            
        Returns:
            True 如果已扫描，False 如果未扫描
        """
        return repo_full_name in self.history["repos"]
    
    def get_scan_info(self, repo_full_name: str) -> Dict:
        """
        获取仓库的扫描信息
        
        Args:
            repo_full_name: 仓库全名 (owner/repo)
            
        Returns:
            扫描信息字典，如果未扫描过则返回 None
        """
        return self.history["repos"].get(repo_full_name)
    
    def mark_as_scanned(self, repo_full_name: str, findings_count: int = 0, 
                        scan_type: str = "unknown"):
        """
        标记仓库为已扫描
        
        Args:
            repo_full_name: 仓库全名 (owner/repo)
            findings_count: 发现的问题数量
            scan_type: 扫描类型
        """
        self.history["repos"][repo_full_name] = {
            "first_scan": self.history["repos"].get(repo_full_name, {}).get(
                "first_scan", 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ),
            "last_scan": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "findings_count": findings_count,
            "scan_type": scan_type,
            "scan_count": self.history["repos"].get(repo_full_name, {}).get("scan_count", 0) + 1
        }
        
        self.history["total_scanned"] = len(self.history["repos"])
        self.history["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        self._save_history()
    
    def get_scanned_repos(self) -> List[str]:
        """
        获取所有已扫描的仓库列表
        
        Returns:
            仓库全名列表
        """
        return list(self.history["repos"].keys())
    
    def get_scanned_count(self) -> int:
        """
        获取已扫描的仓库总数
        
        Returns:
            仓库数量
        """
        return self.history["total_scanned"]
    
    def clear_history(self):
        """清空扫描历史"""
        self.history = {"repos": {}, "total_scanned": 0, "last_updated": None}
        self._save_history()
        print("✅ 扫描历史已清空")
    
    def remove_repo(self, repo_full_name: str):
        """
        从历史记录中移除指定仓库
        
        Args:
            repo_full_name: 仓库全名 (owner/repo)
        """
        if repo_full_name in self.history["repos"]:
            del self.history["repos"][repo_full_name]
            self.history["total_scanned"] = len(self.history["repos"])
            self.history["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self._save_history()
            print(f"✅ 已从历史记录中移除: {repo_full_name}")
        else:
            print(f"⚠️  仓库不在历史记录中: {repo_full_name}")
    
    def get_statistics(self) -> Dict:
        """
        获取扫描统计信息
        
        Returns:
            统计信息字典
        """
        total_findings = sum(
            repo_info.get("findings_count", 0) 
            for repo_info in self.history["repos"].values()
        )
        
        repos_with_findings = sum(
            1 for repo_info in self.history["repos"].values() 
            if repo_info.get("findings_count", 0) > 0
        )
        
        return {
            "total_scanned": self.history["total_scanned"],
            "total_findings": total_findings,
            "repos_with_findings": repos_with_findings,
            "last_updated": self.history["last_updated"]
        }
    
    def print_statistics(self):
        """打印扫描统计信息"""
        stats = self.get_statistics()
        print(f"\n📊 扫描历史统计:")
        print(f"   总扫描仓库数: {stats['total_scanned']}")
        print(f"   发现问题总数: {stats['total_findings']}")
        print(f"   有问题的仓库: {stats['repos_with_findings']}")
        if stats['last_updated']:
            print(f"   最后更新时间: {stats['last_updated']}")

