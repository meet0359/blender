import bpy
print([(p.identifier,p.default if hasattr(p,'default') else '') for p in bpy.types.TriangulateModifier.bl_rna.properties])
