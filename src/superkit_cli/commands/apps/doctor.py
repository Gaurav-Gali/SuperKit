import sys
from pathlib import Path
from superkit.apps.config import AppConfig
from superkit.apps.discovery import discover_apps, get_apps_context
from superkit_cli.utils.project import find_project_root


def doctor_apps():
    print()
    # Project context and root
    apps_path, search_root = get_apps_context()

    if not apps_path or not search_root:
        print(f"  \033[91m✖\033[0m  Not inside a SuperKit project")
        print(f"     \033[90mApps directory not found\033[0m")
        print(f"     \033[90mHint: Ensure you have an 'apps/' directory in your project root or 'src/'\033[0m\n")
        return 1

    # Find project root (one level up from apps or src)
    if apps_path.parent.name == "src":
        project_root = apps_path.parent.parent
        layout = "src-layout"
    else:
        project_root = apps_path.parent
        layout = "flat-layout"

    print(f"  \033[92m✔\033[0m  Project     \033[94m{project_root.name}\033[0m")
    print(f"  \033[92m✔\033[0m  Layout      \033[90m{layout}\033[0m")

    # Apps discovery
    apps = discover_apps()
    app_folders = sorted([d for d in apps_path.iterdir() if d.is_dir() and not d.name.startswith((".", "__"))])

    if not app_folders:
        print(f"\n  \033[93m⚠\033[0m  The apps/ directory is empty\n")
        return 0

    print(f"  \033[92m✔\033[0m  Apps found  \033[90m{len(app_folders)}\033[0m")

    print(f"\n\033[90m" + "─" * 50 + "\033[0m")
    print(f"\033[1mChecking apps...\033[0m\n")

    # Per-app checks
    critical_issues = 0
    warnings = 0
    url_prefixes = {}
    healthy_apps = 0

    for app_dir in app_folders:
        app_name = app_dir.name
        app_issues = []
        is_critical = False

        # 3.1 Folder naming (Python identifier)
        if not app_name.isidentifier():
            app_issues.append("invalid Python identifier (use underscores, not dashes)")
            is_critical = True

        # 3.2 Basic structure
        if not (app_dir / "__init__.py").exists():
            app_issues.append("missing __init__.py")
            is_critical = True

        app_py = app_dir / "app.py"
        if not app_py.exists():
            app_issues.append("missing app.py")
            is_critical = True

        if is_critical:
            print(f"  \033[91m✖\033[0m  \033[1m{app_name}\033[0m")
            for issue in app_issues:
                print(f"     \033[90m└─\033[0m {issue}")
            print()
            critical_issues += len(app_issues)
            continue

        # 3.3 Import & AppConfig validation
        try:
            module = __import__(f"apps.{app_name}.app", fromlist=["*"])
            configs = [
                obj for obj in module.__dict__.values()
                if isinstance(obj, type) and issubclass(obj, AppConfig) and obj is not AppConfig
            ]

            if not configs:
                app_issues.append("no AppConfig class found")
                is_critical = True
            else:
                app_config = configs[0]()

                # AppConfig attributes
                if app_config.name != app_name:
                    app_issues.append(f"name mismatch (config: '{app_config.name}', folder: '{app_name}')")
                    warnings += 1

                if not app_config.url_prefix:
                    app_issues.append("missing url_prefix")
                    is_critical = True
                elif not app_config.url_prefix.startswith("/"):
                    app_issues.append(f"url_prefix should start with '/' (got: '{app_config.url_prefix}')")
                    warnings += 1
                else:
                    if app_config.url_prefix in url_prefixes:
                        url_prefixes[app_config.url_prefix].append(app_name)
                    else:
                        url_prefixes[app_config.url_prefix] = [app_name]

                if not isinstance(app_config.tags, list):
                    app_issues.append("tags should be a list")
                    warnings += 1

                # Router check
                try:
                    router = app_config.build_router()
                    routes = [r for r in router.routes if hasattr(r, 'methods') and r.methods]
                    if not routes:
                        app_issues.append("no routes registered")
                        warnings += 1
                except Exception as e:
                    app_issues.append(f"router build failed ({type(e).__name__})")
                    is_critical = True

        except Exception as e:
            app_issues.append(f"import failed ({type(e).__name__}: {str(e)[:50]})")
            is_critical = True

        # Output app status
        if not app_issues:
            print(f"  \033[92m✔\033[0m  \033[1m{app_name}\033[0m")
            healthy_apps += 1
        else:
            status_icon = "\033[91m✖\033[0m" if is_critical else "\033[93m⚠\033[0m"
            print(f"  {status_icon}  \033[1m{app_name}\033[0m")
            for issue in app_issues:
                issue_prefix = "\033[90m└─\033[0m"
                print(f"     {issue_prefix} {issue}")
            print()
            if is_critical:
                critical_issues += 1

    # Cross-app integrity checks
    if url_prefixes:
        has_duplicates = False
        for prefix, apps_with_prefix in url_prefixes.items():
            if len(apps_with_prefix) > 1:
                if not has_duplicates:
                    print(f"\n\033[90m" + "─" * 50 + "\033[0m")
                    print(f"\033[1mCross-app issues:\033[0m\n")
                    has_duplicates = True
                print(f"  \033[91m✖\033[0m  Duplicate url_prefix \033[93m'{prefix}'\033[0m")
                print(f"     \033[90m└─\033[0m Used by: {', '.join(apps_with_prefix)}")
                print()
                critical_issues += 1

    # Summary
    print(f"\n\033[90m" + "─" * 50 + "\033[0m")
    print(f"\033[1mSummary:\033[0m\n")

    if critical_issues == 0 and warnings == 0:
        print(f"  \033[1m\033[92m✔ All {healthy_apps} app(s) passed health checks\033[0m")
        print(f"  \033[90mEverything looks good. Happy developing.\033[0m\n")
        return 0
    else:
        print(f"  \033[90mHealthy:  \033[0m\033[92m{healthy_apps}\033[0m")
        if critical_issues > 0:
            print(f"  \033[90mCritical: \033[0m\033[91m{critical_issues}\033[0m")
        if warnings > 0:
            print(f"  \033[90mWarnings: \033[0m\033[93m{warnings}\033[0m")

        if critical_issues > 0:
            print(f"\n  \033[90mRun 'superkit apps info <app>' for details\033[0m")

        print()
        return 1 if critical_issues > 0 else 0