from ...core.utils import py3

import os
import configparser
import re


def get_camfile_folder():
    """Get standard path to the folder with IMAQ camera files"""
    public=os.environ.get("PUBLIC","C:\\Users\\Public")
    cam_folder=os.path.join(public,"Documents","National Instruments","NI-IMAQ","Data")
    if os.path.exists(cam_folder):
        return cam_folder
    cam_folder=os.path.join(public,"Public Documents","National Instruments","NI-IMAQ","Data")
    if os.path.exists(cam_folder):
        return cam_folder

def _parse_interface_name(interface):
    interface=py3.as_str(interface)
    if interface.endswith(".iid"):
        interface=interface[:-4]
    if interface.find("::")>-1:
        p=interface.find("::")
        interface,port=interface[:p],int(interface[p+2:])
    else:
        port=0
    return interface,port
def get_interface_file_path(interface):
    """Get path to the interface file based on the interface name (e.g., ``"img1"`` or ```img1::0"``)"""
    cam_folder=get_camfile_folder()
    interface=_parse_interface_name(interface)[0]+".iid"
    path=os.path.join(cam_folder,interface)
    return path if os.path.exists(path) else None
def get_camera_file_path(interface):
    """Get path to the camera file based on the interface name (e.g., ``"img1"`` or ```img1::0"``)"""
    _,port=_parse_interface_name(interface)
    path=get_interface_file_path(interface)
    if path is None:
        return None
    cfg=configparser.ConfigParser()
    cfg.read(path)
    sec="PORT{}".format(port)
    if sec in cfg:
        sec=cfg[sec]
        if "Channel0" in sec:
            name=sec["Channel0"]
            if len(name)>2:
                return name[1:-1]
    return None


def _parse_token(token):
    p=token.find("(")
    return token[:p].strip(), token[p+1:-1].strip()
def _parse_node(text, pos):
    result={}
    last_token=None
    while True:
        m=re.match(r"\s*(}|$)",text[pos:])
        if m is not None:
            pos+=m.end()
            break
        pv,pt,pc=text.find("(",pos),text.find("{",pos),text.find("}",pos)
        if pv<0 and pt<0 and pc<0:
            raise ValueError("can't parse camera file")
        pmin=min([p for p in [pv,pt,pc] if p>=0])
        if pv==pmin:
            if last_token is not None:
                name,value=_parse_token(last_token)
                result[name]=value
            cpv=text.find(")",pv+1)
            last_token=text[pos:cpv+1].strip()
            pos=cpv+1
        elif pt==pmin:
            bname=text[pos:pt].strip()
            if not bname:
                bname=last_token
            elif last_token is not None:
                name,value=_parse_token(last_token)
                result[name]=value
            val,cpt=_parse_node(text,pt+1)
            result[bname]=val
            last_token=None
            pos=cpt+1
        else:
            if last_token is not None:
                name,value=_parse_token(last_token)
                result[name]=value
            result["}"]=text[pos:pc].strip()
            pos=pc
    if last_token is not None:
        name,value=_parse_token(last_token)
        result[name]=value
    return result,pos
def _load_camera_file(cam_file):
    with open(cam_file,"r") as f:
        text=f.read()
    res,pos=_parse_node(text,0)
    if pos!=len(text):
        raise ValueError("can't parse camera file")
    return res

def _format_value(v):
    if isinstance(v,(tuple,list)):
        return str(v)[1:-1]
    else:
        return str(v)
def _write_branch(f, branch, offset):
    pad=" "*(offset*3)
    for n,v in branch.items():
        if isinstance(v,dict):
            f.write("{}{} {{\n".format(pad,n))
            _write_branch(f,v,offset+1)
            f.write("{}}}\n".format(pad))
        elif n!="}":
            f.write("{}{} ({})\n".format(pad,n,_format_value(v)))
    if "}" in branch:
        f.write("{}{}\n".format(pad,branch["}"]))
def _save_camera_file(results, path):
    with open(path,"w") as f:
        _write_branch(f,results,0)




class CameraFile:
    def __init__(self, data=None, path=None):
        self.data=data or {}
        self.path=path
    
    def __getitem__(self, key):
        if isinstance(key,tuple):
            if len(key)==1:
                key=key[0]
            else:
                return self[key[0]][key[1:]]
        if isinstance(key,int):
            key=list(self.data)[key]
        val=self.data[key]
        return CameraFile(val) if isinstance(val,dict) else val
    
    def __setitem__(self, key, value):
        if isinstance(key,tuple):
            if len(key)==1:
                key=key[0]
            else:
                self[key[0]][key[1:]]=value
                return
        if isinstance(key,int):
            key=list(self.data)[key]
        self.data[key]=value
    
    def __contains__(self, key):
        return key in self.data
    def __bool__(self):
        return bool(self.data)
    def __str__(self):
        return "{}({})".format(self.__class__.__name__,self.data)
    __repr__=__str__

    @staticmethod
    def _path_from_cam_name(cam_name):
        if not cam_name.endswith(".icd"):
            cam_name+=".icd"
        cam_folder=get_camfile_folder()
        return os.path.join(cam_folder,cam_name)
    @classmethod
    def from_file(cls, path):
        if not os.path.exists(path):
            return CameraFile()
        return cls(_load_camera_file(path),path=path)
    @classmethod
    def from_camera_file(cls, cam_name):
        return cls.from_file(cls._path_from_cam_name(cam_name))
    @classmethod
    def from_interface(cls, interface):
        cam_name=get_camera_file_path(interface)
        if cam_name is None:
            return cls()
        else:
            return cls.from_camera_file(cam_name)

    def to_file(self, path=None):
        _save_camera_file(self.data,path or self.path)
    def to_camera_file(self, cam_name):
        self.to_file(self._path_from_cam_name(cam_name))
    def to_interface(self, interface):
        cam_name=get_camera_file_path(interface)
        if cam_name is None:
            raise IOError("can't find camera file for interface {}".format(interface))
        else:
            self.to_camera_file(cam_name)