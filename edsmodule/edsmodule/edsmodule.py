#!/home/xingming/pyvirt/bin/python
#-*- coding:utf-8 -*-

#############################################
# File Name: edsmodule.py
# Author: xiaoh
# Mail: p.mars@163.com 
# Created Time:  2016-01-14 17:30:05
#############################################

import sys, os, re, subprocess
import optparse, requests, tarfile, json

parser = optparse.OptionParser()
parser.add_option(
        "-o",
        "--output",
        dest="output",
        help="path for saving module.tar [default:%default]",
        metavar="OUTPUT",
        default=os.getcwd())
parser.add_option(
        "-m",
        "--module",
        dest="module",
        help="module for exporting",
        metavar="MODULE")
parser.add_option(
        "-u",
        "--username",
        dest="username",
        help="username for login",
        metavar="USERNAME")
parser.add_option(
        "-p",
        "--password",
        dest="password",
        help="password for login",
        metavar="PASSWORD")
parser.add_option(
        "-i",
        "--imagetar",
        dest="imagetar",
        help="tar file name of docker images",
        metavar="IMAGETAR")
parser.add_option(
        "-f",
        "--specfile",
        dest="specfile",
        help="tar file name of spec file",
        metavar="SPECFILE")
parser.add_option(
        "-s",
        "--specserver",
        dest="specserver",
        help="host:port of spec server",
        metavar="SPECSERVER")
parser.add_option(
        "-q",
        "--quiet",
        dest="quiet",
        default=False,
        help="don't print logs",
        action="store_false",
        metavar="QUIET")
parser.usage = "%prog command [options]"

(options, args) = parser.parse_args()

output = options.output
module = options.module
username = options.username
password = options.password
imagetar = options.imagetar
specfile = options.specfile
specServer = options.specserver
quiet = options.quiet

pathReg = re.compile('^(.*?)[\\/]?([^\\/]+?)(\.tar)?$')

def edsModule():
    if len(sys.argv) < 2:
        help('please input command(export or import)')
        return
    if sys.argv[1] == 'export':
        edsExport()
    elif sys.argv[1] == 'import':
        edsImport()
    elif sys.argv[1] == 'exportall':
        ExportAll()
    elif sys.argv[1] == 'importall':
        importAll()
    else:
        help('command error, please input command(export or import)')
        return

def edsExport():
    if not module:
        help('please input module name(image name)')
        return
    if not output:
        help('please input output dir')
        return
    if not username:
        help('please input username')
        return
    if not password:
        help('please input password(for login)')
        return
    if not specServer:
        help('please input spec Server')
        return

    mname = pathReg.match(module).group(2)
    specServer = re.compile('^([^:]+)(:[0-9]+)?$').match(specServer).group(1)

    cookies = getCookies(specServer, username, password)
    listURL = 'http://%s/tf/module/list?moduleType=module&keyword=%s' % (specServer, mname)
    r = requests.get(listURL, cookies = cookies)
    if r.ok and r.json()['code'] == 0 and len(r.json()['data']) > 0:
        print 'download code now ...'
        moduleId = r.json()['data'][0]['id']
        downURL = 'http://%s/tf/module/download/%s' % (specServer, moduleId)
        savePath = '%s/%s_code.tar' % (output, mname)
        downloadFile(downURL, savePath, cookies)

    print 'save docker images now ...'
    runCmd('sudo docker save -o %s/%s.tar %s' % (output, mname, module))
    print 'export module over!'

def exportAll():
    if not output:
        help('please input output dir')
        return
    if not username:
        help('please input username')
        return
    if not password:
        help('please input password(for login)')
        return
    if not specServer:
        help('please input spec Server')
        return

    moduleList = getExModules(specServer, username, password)
    for m in moduleList:
        module = m
        edsExport()

def edsImport():
    if not module:
        help('please input module name(image name)')
        return
    if not output:
        help('please input output dir')
        return
    if not username:
        help('please input username')
        return
    if not password:
        help('please input password(for login)')
        return
    if not specServer:
        help('please input spec Server')
        return
    if not imagetar:
        help('please input image tar path')
        return
    if not specfile:
        help('please input spec json file')
        return

    mname = pathReg.match(imagetar).group(2)

    version = 'latest'
    cateTag = 'Basic'
    if specfile:
        t = tarfile.open(specfile, 'r|')
        runCmd('mkdir -p /tmp/spec')
        t.extractall('/tmp/spec')
        addVersion('/tmp/spec/spec.json', 2)
        version = getVersion('/tmp/spec/spec.json')
        cateTag = getCateTag('/tmp/spec/spec.json')
        r = runCmd("cd /tmp/spec && screwjack --username=%s --spec_server=%s submit_import --templateType=%s" % (username, specServer, cateTag))
    if imagetar:
        iid = runCmd('sudo docker import ' + imagetar)
        r = runCmd("sudo docker tag -f %s registry.aps.datacanvas.com:5000/%s/%s:%s" % (iid[0:12], username, mname, version))

def importAll():
    if not output:
        help('please input output dir')
        return
    if not username:
        help('please input username')
        return
    if not password:
        help('please input password(for login)')
        return
    if not specServer:
        help('please input spec Server')
        return
    if not imagetar:
        help('please input image tar path')
        return
    if not specfile:
        help('please input spec json file')
        return

    modules = getImModules(output)
    for m in modules:
        module = m
        edsImport()

def getImModules(output):
    modules = []
    r = re.compile('^(.*)\.tar$')
    for f in os.listdir(output):
        if r.match(f):
            name = r.match(f).group(1)
            if os.path.isfile(output + '/' + name + '_code.tar'):
                modules.append(name)
    return modules

def getExModules(specServer, username, password):
    modules = []
    cookies = getCookies(specServer, username, password)
    downURL = 'http://%s/tf/module/list?page=' % specServer
    for page in range(1, 100):
        url = downURL + str(page)
        js = requests.get(url, cookies=cookies).json()
        if len(js['data']) == 0:
            break
        for m in js['data']:
            modules.append(m['name'])
    return modules

def getCookies(specServer, username, password):
    loginURL = 'http://%s/user/login?account=%s&password=%s' % (specServer, username, password)
    return requests.post(loginURL).cookies

def getVersion(specFile):
    if os.path.isfile(specFile):
        with open(specFile, 'r') as f:
            con = f.read()
        js = json.loads(con)
        return js['Version']
    return 'latest'

def addVersion(specFile, step):
    if os.path.isfile(specFile):
        with open(specFile, 'r') as f:
            con = f.read()
        js = json.loads(con)
        version = js['Version']
        r = re.compile('^(.*?)([0-9]+)$')
        m = r.match(version)
        js['Version'] = m.group(1)+str(int(m.group(2))+step)
        with open(specFile, 'w') as f:
            f.write(json.dumps(js))

def getCateTag(specFile):
    if os.path.isfile(specFile):
        with open(specFile, 'r') as f:
            con = f.read()
    js = json.loads(con)
    if len(js['CategoryTags']) > 0:
        if js['CategoryTags'][0] == 'Basic':
            return 'none'
        return js['CategoryTags'][0].lower()
    return 'none'

def help(msg, t='error'):
    print '[%s] %s' % (t, msg)
    parser.print_help()

def downloadFile(url, savepath, cookies):
    print cookies
    r = requests.get(url, stream=True, cookies=cookies)
    with open(savepath, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                #f.flush() commented by recommendation from J.F.Sebastian
    return savepath

def runCmd(cmd):
    return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()

if __name__ == "__main__":
    edsModule()

