# Copyright 2019 Nokia

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

Name:       lockcli
Version:    %{_version}
Release:    1%{?dist}
Summary:    Contains code for the lock CLI
License:    %{_platform_licence}
Source0:    %{name}-%{version}.tar.gz
Vendor:     %{_platform_vendor}
BuildArch:  noarch

BuildRequires: python
BuildRequires: python-setuptools
Requires: python-etcd
Requires: etcd

%description
This RPM contains source code for the lock cli

%prep
%autosetup

%install
mkdir -p %{buildroot}/%{_python_site_packages_path}/lockcli/
set -e
cd src && python setup.py install --root %{buildroot} --no-compile --install-purelib %{_python_site_packages_path} --install-scripts %{_platform_bin_path} && cd -

%files
%defattr(0755,root,root,0755)
%{_python_site_packages_path}/lockcli*
%{_platform_bin_path}/lockcli

%pre

%post

%preun

%postun

%clean
rm -rf %{buildroot}
