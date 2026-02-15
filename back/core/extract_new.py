#!/usr/bin/env python3
"""
APK Data Extractor - Pure Information Extraction
No labels, no interpretations, just comprehensive facts.
"""

import sys
import os
import re
import json
import hashlib
import zipfile
from typing import Dict, List, Set
from collections import defaultdict

try:
    from androguard.misc import AnalyzeAPK
except ImportError:
    print("ERROR: Install androguard: pip install androguard")
    sys.exit(1)


class APKExtractor:
    """Extracts comprehensive factual information from APK files"""
    
    def __init__(self, apk_path: str):
        self.apk_path = apk_path
        self.apk = None
        self.dalvik = None
        self.analysis = None
    
    def extract(self) -> Dict:
        """Extract all factual information"""
        if not os.path.exists(self.apk_path):
            return {"error": "File not found"}
        
        print(f"Extracting: {self.apk_path}")
        
        try:
            # Load
            print("  Loading APK...")
            self.apk, self.dalvik, self.analysis = AnalyzeAPK(self.apk_path)
            
            data = {
                "basic_info": self._get_basic_info(),
                "manifest": self._get_manifest(),
                "permissions": self._get_permissions(),
                "components": self._get_components(),
                "methods": self._get_methods(),
                "strings": self._get_strings(),
                "files": self._get_files(),
                "bytecode_references": self._get_bytecode_references()
            }
            
            print("  Complete")
            return data
            
        except Exception as e:
            return {"error": str(e)}
    
    def _get_basic_info(self) -> Dict:
        """Get file hashes and basic metadata"""
        print("  Extracting basic info...")
        
        with open(self.apk_path, 'rb') as f:
            content = f.read()
        
        return {
            "file_path": os.path.abspath(self.apk_path),
            "file_size": os.path.getsize(self.apk_path),
            "md5": hashlib.md5(content).hexdigest(),
            "sha256": hashlib.sha256(content).hexdigest(),
            "package_name": self.apk.get_package(),
            "app_name": self.apk.get_app_name(),
            "version_name": getattr(self.apk, 'get_androidversion_name', lambda: None)(),
            "version_code": getattr(self.apk, 'get_androidversion_code', lambda: None)()
        }
    
    def _get_manifest(self) -> Dict:
        """Extract manifest attributes"""
        print("  Parsing manifest...")
        
        manifest_data = {
            "min_sdk": None,
            "target_sdk": None,
            "max_sdk": None,
            "debuggable": False,
            "allow_backup": None,
            "uses_cleartext_traffic": None,
            "network_security_config": None
        }
        
        try:
            manifest_data["min_sdk"] = self.apk.get_min_sdk_version()
            manifest_data["target_sdk"] = self.apk.get_target_sdk_version()
            manifest_data["max_sdk"] = self.apk.get_max_sdk_version()
        except:
            pass
        
        try:
            manifest = self.apk.get_android_manifest_xml()
            app = manifest.find("application")
            ns = "{http://schemas.android.com/apk/res/android}"
            
            if app is not None:
                manifest_data["debuggable"] = app.get(f"{ns}debuggable") == "true"
                manifest_data["allow_backup"] = app.get(f"{ns}allowBackup")
                manifest_data["uses_cleartext_traffic"] = app.get(f"{ns}usesCleartextTraffic")
                manifest_data["network_security_config"] = app.get(f"{ns}networkSecurityConfig")
        except:
            pass
        
        return manifest_data
    
    def _get_permissions(self) -> Dict:
        """Get requested permissions and their usage"""
        print("  Analyzing permissions...")
        
        requested = self.apk.get_permissions()
        
        # Find actual API usage for each permission
        permission_apis = {
            "android.permission.INTERNET": [
                "Ljava/net/Socket;", "Ljava/net/ServerSocket;", "Ljava/net/HttpURLConnection;",
                "Ljava/net/URL;", "Lokhttp3/", "Lretrofit2/"
            ],
            "android.permission.CAMERA": [
                "Landroid/hardware/Camera;", "Landroid/hardware/camera2/"
            ],
            "android.permission.RECORD_AUDIO": [
                "Landroid/media/AudioRecord;", "Landroid/media/MediaRecorder;"
            ],
            "android.permission.ACCESS_FINE_LOCATION": [
                "Landroid/location/LocationManager;", "Lcom/google/android/gms/location/"
            ],
            "android.permission.ACCESS_COARSE_LOCATION": [
                "Landroid/location/LocationManager;", "Lcom/google/android/gms/location/"
            ],
            "android.permission.READ_CONTACTS": [
                "Landroid/provider/ContactsContract;"
            ],
            "android.permission.READ_SMS": [
                "Landroid/provider/Telephony;", "content://sms"
            ],
            "android.permission.SEND_SMS": [
                "Landroid/telephony/SmsManager;->sendTextMessage"
            ],
            "android.permission.READ_PHONE_STATE": [
                "Landroid/telephony/TelephonyManager;->getDeviceId",
                "Landroid/telephony/TelephonyManager;->getSubscriberId"
            ],
            "android.permission.WRITE_EXTERNAL_STORAGE": [
                "Landroid/os/Environment;->getExternalStorageDirectory"
            ],
            "android.permission.READ_EXTERNAL_STORAGE": [
                "Landroid/os/Environment;->getExternalStorageDirectory"
            ]
        }
        
        # Collect all APIs used in bytecode
        all_apis = self._collect_all_apis()
        
        # Map usage
        usage = {}
        for perm in requested:
            if perm in permission_apis:
                patterns = permission_apis[perm]
                found = [api for api in all_apis if any(p in api for p in patterns)]
                usage[perm] = {
                    "requested": True,
                    "apis_found": found[:10],  # Limit output
                    "api_count": len(found)
                }
            else:
                usage[perm] = {"requested": True}
        
        return {
            "requested": requested,
            "usage": usage
        }
    
    def _collect_all_apis(self) -> Set[str]:
        """Collect all API calls from bytecode"""
        apis = set()
        
        if not self.dalvik:
            return apis
        
        for dex in self.dalvik:
            for cls in dex.get_classes():
                for method in cls.get_methods():
                    try:
                        mx = self.analysis.get_method(method)
                        if mx:
                            for call in mx.get_xref_to():
                                called_class = call[0].get_class_name()
                                called_method = call[0].get_name()
                                apis.add(f"{called_class}->{called_method}")
                    except:
                        continue
        
        return apis
    
    def _get_components(self) -> Dict:
        """Extract Android components with emphasis on exported ones"""
        print("  Extracting components...")
        
        components = {
            "activities": [],
            "services": [],
            "receivers": [],
            "providers": [],
            "exported_summary": {
                "exported_activities": [],
                "exported_services": [],
                "exported_receivers": [],
                "exported_providers": []
            }
        }
        
        try:
            manifest = self.apk.get_android_manifest_xml()
            ns = "{http://schemas.android.com/apk/res/android}"
            
            for activity in manifest.iter("activity"):
                name = activity.get(f"{ns}name")
                exported = activity.get(f"{ns}exported")
                permission = activity.get(f"{ns}permission")
                
                info = {
                    "name": name,
                    "exported": exported,
                    "permission": permission
                }
                components["activities"].append(info)
                
                # Track exported components
                if exported == "true":
                    components["exported_summary"]["exported_activities"].append({
                        "name": name,
                        "permission": permission
                    })
            
            for service in manifest.iter("service"):
                name = service.get(f"{ns}name")
                exported = service.get(f"{ns}exported")
                permission = service.get(f"{ns}permission")
                
                info = {
                    "name": name,
                    "exported": exported,
                    "permission": permission
                }
                components["services"].append(info)
                
                if exported == "true":
                    components["exported_summary"]["exported_services"].append({
                        "name": name,
                        "permission": permission
                    })
            
            for receiver in manifest.iter("receiver"):
                name = receiver.get(f"{ns}name")
                exported = receiver.get(f"{ns}exported")
                permission = receiver.get(f"{ns}permission")
                
                info = {
                    "name": name,
                    "exported": exported,
                    "permission": permission
                }
                components["receivers"].append(info)
                
                if exported == "true":
                    components["exported_summary"]["exported_receivers"].append({
                        "name": name,
                        "permission": permission
                    })
            
            for provider in manifest.iter("provider"):
                name = provider.get(f"{ns}name")
                exported = provider.get(f"{ns}exported")
                authorities = provider.get(f"{ns}authorities")
                permission = provider.get(f"{ns}permission")
                
                info = {
                    "name": name,
                    "exported": exported,
                    "authorities": authorities,
                    "permission": permission
                }
                components["providers"].append(info)
                
                if exported == "true":
                    components["exported_summary"]["exported_providers"].append({
                        "name": name,
                        "authorities": authorities,
                        "permission": permission
                    })
        except:
            pass
        
        return components
    
    def _get_methods(self) -> Dict:
        """Get class and method statistics"""
        print("  Analyzing code structure...")
        
        if not self.dalvik:
            return {}
        
        stats = {
            "total_classes": 0,
            "total_methods": 0,
            "classes_by_package": defaultdict(int)
        }
        
        package_name = self.apk.get_package()
        app_prefix = f"L{package_name.replace('.', '/')}/" if package_name else None
        
        for dex in self.dalvik:
            for cls in dex.get_classes():
                stats["total_classes"] += 1
                class_name = cls.get_name()
                
                # Count by package
                if '/' in class_name:
                    pkg = '/'.join(class_name.split('/')[:-1])
                    stats["classes_by_package"][pkg] += 1
                
                # Count methods
                stats["total_methods"] += len(list(cls.get_methods()))
        
        # Top packages
        top = sorted(stats["classes_by_package"].items(), key=lambda x: x[1], reverse=True)[:10]
        stats["top_packages"] = dict(top)
        del stats["classes_by_package"]
        
        return stats
    
    def _get_strings(self) -> Dict:
        """Extract and categorize strings, filtering out generic schemas"""
        print("  Extracting strings...")
        
        if not self.analysis:
            return {}
        
        strings = {
            "urls": [],
            "ip_addresses": [],
            "file_paths": [],
            "base64_candidates": []
        }
        
        # Generic/benign URL patterns to filter out
        generic_url_patterns = [
            'schemas.android.com',
            'schema.org',
            'w3.org',
            'xmlpull.org',
            'apache.org/xml',
            'xmlns',
            'googleads',
            'googleapis.com/auth',
            'gstatic.com',
            'android.com',
            'google.com/schemas',
            'java.sun.com',
            'xml.org'
        ]
        
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        
        seen_urls = set()
        seen_ips = set()
        
        for s_obj in self.analysis.get_strings():
            s = s_obj.get_value()
            if not s or len(s) < 4:
                continue
            
            # URLs - with filtering
            urls = re.findall(url_pattern, s)
            for url in urls:
                if url not in seen_urls:
                    # Filter out generic schemas and definitions
                    is_generic = any(pattern in url.lower() for pattern in generic_url_patterns)
                    
                    if not is_generic:
                        seen_urls.add(url)
                        strings["urls"].append(url)
            
            # IPs - keep EVERY SINGLE ONE (no filtering whatsoever)
            ips = re.findall(ip_pattern, s)
            for ip in ips:
                if ip not in seen_ips:
                    # Validate it's a proper IP format
                    try:
                        parts = [int(p) for p in ip.split('.')]
                        if all(0 <= p <= 255 for p in parts):
                            seen_ips.add(ip)
                            strings["ip_addresses"].append(ip)
                    except:
                        pass
            
            # File paths
            if s.startswith('/') and len(s) > 5:
                if '/' in s[1:]:
                    strings["file_paths"].append(s)
            
            # Base64 candidates - suspicious strings
            if len(s) > 30 and re.match(r'^[A-Za-z0-9+/=]+$', s):
                # Must end with = or == (proper base64 padding)
                if s.endswith('=') or s.endswith('=='):
                    # Calculate length - should be multiple of 4
                    if len(s) % 4 == 0:
                        strings["base64_candidates"].append(s[:100])
        
        # Deduplicate and limit
        strings["urls"] = list(set(strings["urls"]))[:100]
        strings["ip_addresses"] = list(set(strings["ip_addresses"]))[:50]
        strings["file_paths"] = list(set(strings["file_paths"]))[:100]
        strings["base64_candidates"] = list(set(strings["base64_candidates"]))[:50]
        
        return strings
    
    def _get_files(self) -> Dict:
        """Get file listing from APK, filtering out standard resources"""
        print("  Listing files...")
        
        try:
            with zipfile.ZipFile(self.apk_path, 'r') as z:
                all_files = z.namelist()
                
                # Filter resources - remove standard Android resource types
                filtered_resources = []
                standard_res_prefixes = [
                    'res/drawable',
                    'res/anim',
                    'res/color',
                    'res/layout',
                    'res/mipmap'
                ]
                
                for f in all_files:
                    if f.startswith('res/'):
                        # Skip standard resource types
                        if not any(f.startswith(prefix) for prefix in standard_res_prefixes):
                            filtered_resources.append(f)
                
                # Suspicious file patterns
                suspicious_extensions = ['.sh', '.bin', '.elf', '.jar', '.apk', '.zip']
                suspicious_files = [f for f in all_files 
                                   if any(f.endswith(ext) for ext in suspicious_extensions)
                                   and not f.startswith('lib/')]
                
                return {
                    "total_files": len(all_files),
                    "dex_files": [f for f in all_files if f.endswith('.dex')],
                    "native_libs": [f for f in all_files if f.endswith('.so')],
                    "suspicious_files": suspicious_files,
                    "non_standard_resources": filtered_resources,
                    "assets": [f for f in all_files if f.startswith('assets/')]
                }
        except:
            return {}
    
    def _get_bytecode_references(self) -> Dict:
        """Get specific bytecode references of interest"""
        print("  Scanning bytecode...")
        
        if not self.dalvik:
            return {}
        
        refs = {
            "network_operations": [],
            "file_operations": [],
            "crypto_operations": [],
            "reflection_usage": [],
            "runtime_exec": [],
            "dynamic_loading": []
        }
        
        package_name = self.apk.get_package()
        app_prefix = f"L{package_name.replace('.', '/')}/" if package_name else None
        
        for dex in self.dalvik:
            for cls in dex.get_classes():
                class_name = cls.get_name()
                
                # Check if this is app's own code
                is_app_code = app_prefix and class_name.startswith(app_prefix)
                
                for method in cls.get_methods():
                    try:
                        mx = self.analysis.get_method(method)
                        if not mx:
                            continue
                        
                        for call in mx.get_xref_to():
                            called = f"{call[0].get_class_name()}->{call[0].get_name()}"
                            location = f"{class_name}.{method.get_name()}"
                            
                            ref = {
                                "api": called,
                                "called_from": location,
                                "in_app_code": is_app_code
                            }
                            
                            # Categorize
                            if any(x in called for x in ["Socket", "HttpURLConnection", "URL;->openConnection"]):
                                refs["network_operations"].append(ref)
                            elif any(x in called for x in ["FileInputStream", "FileOutputStream", "File;->delete"]):
                                refs["file_operations"].append(ref)
                            elif any(x in called for x in ["Cipher", "MessageDigest", "SecretKey"]):
                                refs["crypto_operations"].append(ref)
                            elif "reflect" in called.lower():
                                refs["reflection_usage"].append(ref)
                            elif "Runtime;->exec" in called or "ProcessBuilder" in called:
                                refs["runtime_exec"].append(ref)
                            elif any(x in called for x in ["DexClassLoader", "DexFile", "PathClassLoader"]):
                                refs["dynamic_loading"].append(ref)
                    except:
                        continue
        
        # Deduplicate
        for key in refs:
            seen = set()
            unique = []
            for item in refs[key]:
                sig = f"{item['api']}:{item['called_from']}"
                if sig not in seen:
                    seen.add(sig)
                    unique.append(item)
            refs[key] = unique[:50]  # Limit per category
        
        return refs


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract.py <apk_file> [output.json]")
        sys.exit(1)
    
    apk_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "apk_data.json"
    
    extractor = APKExtractor(apk_path)
    data = extractor.extract()
    
    # Save
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    if "error" in data:
        print(f"\nError: {data['error']}")
    else:
        print(f"\nSaved to: {output_path}")
        print("\n" + "="*60)
        print("EXTRACTION SUMMARY")
        print("="*60)
        print(f"Package: {data['basic_info']['package_name']}")
        print(f"Version: {data['basic_info']['version_name']}")
        print(f"\n--- PERMISSIONS ---")
        print(f"Total requested: {len(data['permissions']['requested'])}")
        used_perms = [p for p, info in data['permissions']['usage'].items() 
                     if info.get('api_count', 0) > 0]
        print(f"Actually used: {len(used_perms)}")
        if len(used_perms) < len(data['permissions']['requested']):
            unused = len(data['permissions']['requested']) - len(used_perms)
            print(f"Unused (potential ghost): {unused}")
        
        print(f"\n--- COMPONENTS ---")
        print(f"Activities: {len(data['components']['activities'])}")
        print(f"Services: {len(data['components']['services'])}")
        print(f"Receivers: {len(data['components']['receivers'])}")
        print(f"Providers: {len(data['components']['providers'])}")
        
        # Highlight exported components
        exp_act = len(data['components']['exported_summary']['exported_activities'])
        exp_svc = len(data['components']['exported_summary']['exported_services'])
        exp_rec = len(data['components']['exported_summary']['exported_receivers'])
        exp_prv = len(data['components']['exported_summary']['exported_providers'])
        total_exported = exp_act + exp_svc + exp_rec + exp_prv
        
        if total_exported > 0:
            print(f"\n⚠️  EXPORTED COMPONENTS: {total_exported}")
            if exp_act > 0:
                print(f"  • Exported Activities: {exp_act}")
            if exp_svc > 0:
                print(f"  • Exported Services: {exp_svc}")
            if exp_rec > 0:
                print(f"  • Exported Receivers: {exp_rec}")
            if exp_prv > 0:
                print(f"  • Exported Providers: {exp_prv}")
        
        print(f"\n--- CODE STRUCTURE ---")
        print(f"Classes: {data['methods']['total_classes']}")
        print(f"Methods: {data['methods']['total_methods']}")
        
        print(f"\n--- BYTECODE REFERENCES ---")
        print(f"Network ops: {len(data['bytecode_references']['network_operations'])}")
        print(f"Crypto ops: {len(data['bytecode_references']['crypto_operations'])}")
        print(f"Runtime exec: {len(data['bytecode_references']['runtime_exec'])}")
        print(f"Dynamic loading: {len(data['bytecode_references']['dynamic_loading'])}")
        
        print(f"\n--- STRINGS (FILTERED) ---")
        print(f"URLs: {len(data['strings']['urls'])} (generic schemas removed)")
        print(f"IP addresses: {len(data['strings']['ip_addresses'])}")
        print(f"Base64 candidates: {len(data['strings']['base64_candidates'])}")
        
        # Highlight if suspicious
        if len(data['strings']['ip_addresses']) > 0:
            print(f"\n⚠️  HARDCODED IP ADDRESSES FOUND: {len(data['strings']['ip_addresses'])}")
            for ip in data['strings']['ip_addresses'][:5]:
                print(f"  • {ip}")
        
        if len(data['strings']['base64_candidates']) > 5:
            print(f"\n⚠️  SUSPICIOUS BASE64 STRINGS: {len(data['strings']['base64_candidates'])}")
        
        print(f"\n--- FILES (FILTERED) ---")
        print(f"Total files: {data['files']['total_files']}")
        print(f"DEX files: {len(data['files']['dex_files'])}")
        print(f"Native libraries: {len(data['files']['native_libs'])}")
        
        suspicious = data['files'].get('suspicious_files', [])
        if suspicious:
            print(f"\n⚠️  SUSPICIOUS FILES: {len(suspicious)}")
            for f in suspicious[:5]:
                print(f"  • {f}")
        
        non_standard_res = data['files'].get('non_standard_resources', [])
        if non_standard_res:
            print(f"\nNon-standard resources: {len(non_standard_res)}")
        
        print("="*60)


if __name__ == "__main__":
    main()
