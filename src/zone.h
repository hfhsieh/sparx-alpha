#ifndef __ZONE_H__
#define __ZONE_H__

#include <stdio.h>
#include "geometry.h"

typedef struct Zone {
	/* Grid level */
	int level;

	/* 1-D position of this zone relative to current level */
	size_t pos;

	/* 3-D position of this zone */
	GeVec3_s index;

	/* GeVox associated with this zone */
	GeVox voxel;

	/* Pointers to parent and children */
	struct Zone *root, *parent, **children;

	/* Number of children */
	size_t nchildren;

	/* Number of divisions on each axis on child grid */
	GeVec3_s naxes;

	/* Generic pointer to data associated with this zone */
	void *data;

} Zone;

#define Zone_CHILD(zone, idx)\
	zone->children[Ge_IndexToIelem(&(idx), &(zone)->naxes)]

#define Zone_CHILD2(zone, i, j, k)\
	zone->children[Ge_PosToIelem((size_t)(i), (size_t)(j), (size_t)k, &(zone)->naxes)]

/* Zone utility routines */
Zone *_Zone_Alloc(size_t pos, Zone *parent, void *(*DataAlloc)(const Zone *, const void *), const void *data_parms);
#define Zone_Alloc(pos, parent, DataAlloc, data_parms)\
	_Zone_Alloc((size_t)(pos), (parent), (DataAlloc), (data_parms))
void Zone_Free(void *ptr, void (*DataFree)(void *ptr));
void Zone_GrowChildren(Zone *zone, GeVec3_s naxes, void *(*DataAlloc)(const Zone *, const void *), const void *data_parms);
void Zone_Set_child_voxel(Zone *zone, size_t pos);

Zone *Zone_GetLeaf(Zone *zone, size_t side, const GeVec3_d *pt, const GeRay *ray);
Zone *Zone_GetLeaf_sph1d(Zone *zone, size_t side);
Zone *Zone_GetLeaf_sph3d(Zone *zone, size_t side, const GeVec3_d *pt, const GeRay *ray);
Zone *Zone_GetLeaf_rec3d(Zone *zone, size_t side, const GeVec3_d *pt);
Zone *Zone_GetLeaf_cyl3d(Zone *zone, size_t side, const GeVec3_d *pt, const GeRay *ray);

Zone *Zone_GetNext_sph1d(Zone *zone, size_t *side, const GeVec3_d *pt);
Zone *Zone_GetNext_sph3d(Zone *zone, size_t *side, const GeVec3_d *pt, const GeRay *ray);
Zone *Zone_GetNext_rec3d(Zone *zone, size_t side, const GeVec3_d *pt);
Zone *Zone_GetNext_cyl3d(Zone *zone, size_t *side, const GeVec3_d *pt, const GeRay *ray);

Zone *Zone_GetMinLeaf(Zone *zone);
Zone *Zone_GetMaxLeaf(Zone *zone);
Zone *Zone_GetInner(Zone *zone, const GeVec3_d *pt);
Zone *Zone_GetOuter(Zone *zone);
Zone *Zone_AscendTree(Zone *zone);

/* Zone display/print routines */
void Zone_Fprintf(FILE *fp, const Zone *zone, void (*DataFprintf)(void *data, FILE *fp));
void Zone_Cpgplot(Zone *zone, GeCam *cam);

size_t Zone_Fwrite(const Zone *zone, size_t (*DataFwrite)(void *data, FILE *fp), FILE *fp);
Zone *Zone_Fread(void *(*DataAlloc)(const void *data_parms), const void *data_parms,
	size_t (*DataFread)(void *data, FILE *fp), FILE *fp);

Zone *Zone_GetNext(Zone *zone, size_t *plane, const GeRay *ray);


size_t ZoneIndex( GEOM_TYPE geom, size_t i, size_t j, size_t k, Zone * root);

double Zone_ZoneSize(Zone *zp);

#endif



