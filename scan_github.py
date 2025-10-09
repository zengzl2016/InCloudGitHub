#!/usr/bin/env python3
"""
InCloud GitHub 云上扫描器 - 主程序
用于扫描GitHub仓库中泄露的AI API密钥和敏感信息
"""
import argparse
import sys
import os
from datetime import datetime
from config import GITHUB_TOKEN
from scanner import CloudScanner


def print_banner():
    """打印程序横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        InCloud GitHub 云上扫描器                          ║
║        AI API Key Leakage Scanner                         ║
║                                                           ║
║        Version: 1.0.0                                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def validate_github_token() -> bool:
    """验证GitHub Token是否存在"""
    if not GITHUB_TOKEN:
        print("❌ 错误: 未找到 GitHub Token")
        print("\n请按以下步骤设置：")
        print("1. 复制 .env.example 为 .env")
        print("2. 在 https://github.com/settings/tokens 创建 Personal Access Token")
        print("3. 将 Token 添加到 .env 文件中的 GITHUB_TOKEN 变量")
        return False
    return True


def main():
    """主函数"""
    print_banner()
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description='扫描 GitHub 仓库中泄露的 AI API 密钥和敏感信息',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 扫描指定用户的所有公开仓库
  python scan_github.py --user username
  
  # 扫描指定组织的所有公开仓库
  python scan_github.py --org organization_name
  
  # 扫描单个仓库
  python scan_github.py --repo owner/repo_name
  
  # 自动搜索并扫描 AI 相关项目
  python scan_github.py --auto
  
  # 自动搜索并扫描指定数量的仓库
  python scan_github.py --auto --max-repos 100
        """
    )
    
    # 添加参数
    parser.add_argument(
        '--user',
        type=str,
        help='扫描指定 GitHub 用户的所有公开仓库'
    )
    
    parser.add_argument(
        '--org',
        type=str,
        help='扫描指定 GitHub 组织的所有公开仓库'
    )
    
    parser.add_argument(
        '--repo',
        type=str,
        help='扫描单个仓库 (格式: owner/repo_name)'
    )
    
    parser.add_argument(
        '--auto',
        action='store_true',
        help='自动搜索并扫描 AI 相关项目'
    )
    
    parser.add_argument(
        '--max-repos',
        type=int,
        default=50,
        help='自动模式下最大扫描仓库数 (默认: 50)'
    )
    
    parser.add_argument(
        '--token',
        type=str,
        help='GitHub Personal Access Token (可选，默认从 .env 读取)'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        help='报告输出目录 (可选，默认: ./scan_reports)'
    )
    
    parser.add_argument(
        '--no-skip-scanned',
        action='store_true',
        help='不跳过已扫描的仓库，强制重新扫描所有仓库'
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 检查是否提供了至少一个扫描选项
    if not any([args.user, args.org, args.repo, args.auto]):
        parser.print_help()
        print("\n❌ 错误: 请至少指定一个扫描选项 (--user, --org, --repo, 或 --auto)")
        sys.exit(1)
    
    # 验证 GitHub Token
    token = args.token or GITHUB_TOKEN
    if not token:
        if not validate_github_token():
            sys.exit(1)
    
    # 设置输出目录
    if args.output_dir:
        os.environ['OUTPUT_DIR'] = args.output_dir
    
    try:
        # 创建扫描器实例
        skip_scanned = not args.no_skip_scanned
        scanner = CloudScanner(token, skip_scanned=skip_scanned)
        
        # 根据参数执行不同的扫描
        if args.user:
            report_path = scanner.scan_user(args.user)
        elif args.org:
            report_path = scanner.scan_organization(args.org)
        elif args.repo:
            report_path = scanner.scan_single_repo(args.repo)
        elif args.auto:
            report_path = scanner.scan_ai_projects(max_repos=args.max_repos)
        
        print(f"\n✅ 扫描完成！")
        print(f"📄 报告已保存至: {report_path}")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断扫描")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 扫描过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
