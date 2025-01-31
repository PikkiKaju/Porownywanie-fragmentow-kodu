#include<limits.h>
#include<stdlib.h>
#include<stdio.h>

typedef struct{
    int sourceVertex, destVertex;
    int edgeWeight;
}edge;

typedef struct{
    int vertices, edges;
    edge* edgeMatrix;
}graph;

void floydWarshall(graph g){
    int processWeights[g.vertices][g.vertices], processedVertices[g.vertices][g.vertices];
    int i,j,k;
    
    for(i=0;i<g.vertices;i++)
        for(j=0;j<g.vertices;j++){
            processWeights[i][j] = SHRT_MAX;
            processedVertices[i][j] = (i!=j)?j+1:0;
        }
        
    for(i=0;i<g.edges;i++)
        processWeights[g.edgeMatrix[i].sourceVertex-1][g.edgeMatrix[i].destVertex-1] = g.edgeMatrix[i].edgeWeight;
        
    for(i=0;i<g.vertices;i++)
        for(j=0;j<g.vertices;j++)
            for(k=0;k<g.vertices;k++){
                if(processWeights[j][i] + processWeights[i][k] < processWeights[j][k]){
                    processWeights[j][k] = processWeights[j][i] + processWeights[i][k];
                    processedVertices[j][k] = processedVertices[j][i];
                }
            }
        
    printf("pair    dist   path");
    for(i=0;i<g.vertices;i++)
        for(j=0;j<g.vertices;j++){
            if(i!=j){
                printf("\n%d -> %d %3d %5d",i+1,j+1,processWeights[i][j],i+1);
                k = i+1;
                do{
                    k = processedVertices[k-1][j];
                    printf("->%d",k);
                }while(k!=j+1);
            }
        }
}