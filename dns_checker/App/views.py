# import ssl
# import dns.resolver
# import socket
# from django.shortcuts import render
# from datetime import datetime

# def check_dns_and_ssl(request):
#     if request.method == 'POST':
#         domain = request.POST.get('domain')

#         # DNS Lookup for all IPv4 addresses
#         try:
#             dns_info = dns.resolver.resolve(domain, 'A')  # Get all A records
#             ip_addresses = [str(record) for record in dns_info]
#         except Exception as e:
#             ip_addresses = [f"DNS lookup failed: {e}"]

#         # SSL Check
#         ssl_details = {}
#         try:
#             # SSL connection setup
#             context = ssl.create_default_context()
#             with socket.create_connection((domain, 443)) as sock:
#                 with context.wrap_socket(sock, server_hostname=domain) as ssock:
#                     cert = ssock.getpeercert()

#             # Extract SSL certificate details
#             not_before = cert['notBefore']
#             not_after = cert['notAfter']
#             issuer = dict(x[0] for x in cert['issuer'])

#             ssl_details['notBefore'] = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
#             ssl_details['notAfter'] = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
#             ssl_details['is_valid'] = ssl_details['notAfter'] > datetime.utcnow()
#             ssl_details['issuer'] = issuer
#         except Exception as e:
#             ssl_details['error'] = f"SSL check failed: {e}"

#         context = {
#             'ip_addresses': ip_addresses,
#             'ssl_details': ssl_details,
#         }
#         return render(request, 'App/result.html', context)

#     return render(request, 'App/index.html')

import ssl
import dns.resolver
import socket
from django.shortcuts import render
from datetime import datetime

def check_dns_and_ssl(request):
    response_issues = {}
    
    if request.method == 'POST':
        domain = request.POST.get('domain')

        # DNS Lookup for all IPv4 addresses
        try:
            dns_info = dns.resolver.resolve(domain, 'A')
            ip_addresses = [str(record) for record in dns_info]
        except Exception as e:
            ip_addresses = []
            response_issues['DNS Error'] = str(e)

        # SSL Check
        ssl_details = {}
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()

            # Extract SSL certificate details
            not_before = cert['notBefore']
            not_after = cert['notAfter']
            issuer = dict(x[0] for x in cert['issuer'])

            ssl_details['notBefore'] = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
            ssl_details['notAfter'] = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            ssl_details['is_valid'] = ssl_details['notAfter'] > datetime.utcnow()
            ssl_details['issuer'] = issuer
        except Exception as e:
            ssl_details = {}
            response_issues['SSL Error'] = str(e)

        context = {
            'ip_addresses': ip_addresses,
            'ssl_details': ssl_details,
            'response_issues': response_issues,
        }
        return render(request, 'App/result.html', context)

    return render(request, 'App/index.html')
