import os
import stl
from stl import mesh
import subprocess


class OpenSCAD(object):
    """Management class for OpenSCAD command line interface"""
    def __init__(self):
        pass

    def get_version(self):
        """return installed OpenScAD version"""
        result = subprocess.run(['openscad','--version'], capture_output=True)
        version = result.stderr.decode().split()[2]
        return version

    def gen_stl(self, scad_path):
        """ Generate STL file from specified SCAD file"""
        err_code = 1
        if not os.path.isfile(scad_path):
            return err_code
        if scad_path.endswith(".scad"):
            base, ext = scad_path.split(".")
            stl_path = base  + ".stl"
            cmd = [
                'openscad',
                scad_path,
                "-o",
                stl_path
            ]

            result = subprocess.run(cmd, capture_output=True)
            err_code = result.returncode
            if not os.path.isfile(stl_path) or err_code != 0: # pragma: no cover
                err_code = 1
        return err_code

    def _get_bounds(self):
        """set internal bounds variables"""
        minx = maxx = miny = maxy = minz = maxz = None
        obj = self.mesh
        for p in obj.points:
            # p contains (x, y, z)
            if minx is None:
                minx = p[stl.Dimension.X]
                maxx = p[stl.Dimension.X]
                miny = p[stl.Dimension.Y]
                maxy = p[stl.Dimension.Y]
                minz = p[stl.Dimension.Z]
                maxz = p[stl.Dimension.Z]
            else:
                maxx = max(p[stl.Dimension.X], maxx)
                minx = min(p[stl.Dimension.X], minx)
                maxy = max(p[stl.Dimension.Y], maxy)
                miny = min(p[stl.Dimension.Y], miny)
                maxz = max(p[stl.Dimension.Z], maxz)
                minz = min(p[stl.Dimension.Z], minz)
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz

    def dump_to_json(self, json_path):
        """write mas properties data to specified JSON file"""
        json = "{\n"
        json += '  "maxx": "%s",\n' % self.maxx
        json += '  "minx": "%s",\n' % self.minx
        json += '  "maxy": "%s",\n' % self.maxy
        json += '  "miny": "%s",\n' % self.miny
        json += '  "maxz": "%s",\n' % self.maxz
        json += '  "minz": "%s",\n' % self.minz
        json += '  "volume": "%s",\n' % self.volume
        json += '  "cgx": "%s",\n' % self.cgx
        json += '  "cgy": "%s",\n' % self.cgy
        json += '  "cgz": "%s",\n' % self.cgz
        json += '  "ixx": "%s",\n' % self.ixx
        json += '  "ixy": "%s",\n' % self.ixy
        json += '  "ixz": "%s",\n' % self.ixz
        json += '  "iyx": "%s",\n' % self.iyx
        json += '  "iyy": "%s",\n' % self.iyy
        json += '  "iyz": "%s",\n' % self.iyz
        json += '  "izx": "%s",\n' % self.izx
        json += '  "izy": "%s",\n' % self.izy
        json += '  "izz": "%s"\n' % self.izz
        json += '}\n'

        with open(json_path,'w') as fout:
            fout.write(json)


    def get_properties(self, scad_file):
        """Calculate mass properties from specified SCAD file"""
        scad_path = os.path.abspath(scad_file)
        err_code = self.gen_stl(scad_path)
        base, ext = scad_path.split(".")
        stl_file = base + ".stl"
        self.json_file = base + ".json"
        self.mesh = mesh.Mesh.from_file(stl_file)
        self._get_bounds()
        volume, cog, inertia = self.mesh.get_mass_properties()
        self.cgx, self.cgy, self.cgz = cog
        self.volume = volume
        self.ixx, self.ixy, self.ixz = inertia[0]
        self.iyx, self.iyy, self.iyz = inertia[1]
        self.izx, self.izy, self.izz = inertia[2]
        return err_code

    def get_bounds(self):
        """Return bounds data as a list"""
        return [
                self.maxx, self.minx,
                self.maxy, self.miny,
                self.maxz, self.minz
        ]

if __name__ == '__main__':
    mgr = OpenSCAD()
    print(mgr.get_version())
    mgr.get_properties("../tests/test_data/spar.scad")
    mgr.dump_to_json("../tests/test_data/spar.json")


