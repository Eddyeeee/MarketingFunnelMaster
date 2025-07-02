import React, { useState } from 'react';
import { ChevronRight, ChevronDown, File, Folder, FolderOpen } from 'lucide-react';
import { cn } from '@/lib/utils';

export interface TreeNode {
  id: string;
  label: string;
  children?: TreeNode[];
  data?: any;
  icon?: React.ReactNode;
  expanded?: boolean;
  selected?: boolean;
}

interface TreeViewProps {
  data: TreeNode[];
  onSelect?: (node: TreeNode) => void;
  onExpand?: (nodeId: string, expanded: boolean) => void;
  className?: string;
  showIcons?: boolean;
  multiSelect?: boolean;
}

interface TreeNodeProps {
  node: TreeNode;
  level: number;
  onSelect?: (node: TreeNode) => void;
  onExpand?: (nodeId: string, expanded: boolean) => void;
  showIcons?: boolean;
  selectedIds: Set<string>;
  expandedIds: Set<string>;
}

function TreeNodeComponent({
  node,
  level,
  onSelect,
  onExpand,
  showIcons = true,
  selectedIds,
  expandedIds,
}: TreeNodeProps) {
  const hasChildren = node.children && node.children.length > 0;
  const isExpanded = expandedIds.has(node.id);
  const isSelected = selectedIds.has(node.id);

  const handleToggle = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (hasChildren) {
      onExpand?.(node.id, !isExpanded);
    }
  };

  const handleSelect = () => {
    onSelect?.(node);
  };

  const getIcon = () => {
    if (node.icon) return node.icon;
    if (!showIcons) return null;
    
    if (hasChildren) {
      return isExpanded ? (
        <FolderOpen className="h-4 w-4 text-blue-500" />
      ) : (
        <Folder className="h-4 w-4 text-blue-500" />
      );
    }
    return <File className="h-4 w-4 text-gray-500" />;
  };

  return (
    <div className="select-none">
      <div
        className={cn(
          'flex items-center py-1 px-2 rounded cursor-pointer hover:bg-muted/50 transition-colors',
          isSelected && 'bg-primary/10 text-primary',
          'group'
        )}
        style={{ paddingLeft: `${level * 16 + 8}px` }}
        onClick={handleSelect}
      >
        <div className="flex items-center flex-1 min-w-0">
          {hasChildren ? (
            <button
              onClick={handleToggle}
              className="flex items-center justify-center w-4 h-4 mr-1 hover:bg-muted rounded"
            >
              {isExpanded ? (
                <ChevronDown className="h-3 w-3" />
              ) : (
                <ChevronRight className="h-3 w-3" />
              )}
            </button>
          ) : (
            <div className="w-4 h-4 mr-1" />
          )}
          
          {showIcons && (
            <div className="mr-2 flex-shrink-0">
              {getIcon()}
            </div>
          )}
          
          <span
            className={cn(
              'text-sm truncate flex-1',
              isSelected && 'font-medium'
            )}
            title={node.label}
          >
            {node.label}
          </span>
        </div>
      </div>

      {hasChildren && isExpanded && (
        <div className="ml-2">
          {node.children!.map((child) => (
            <TreeNodeComponent
              key={child.id}
              node={child}
              level={level + 1}
              onSelect={onSelect}
              onExpand={onExpand}
              showIcons={showIcons}
              selectedIds={selectedIds}
              expandedIds={expandedIds}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export function TreeView({
  data,
  onSelect,
  onExpand,
  className,
  showIcons = true,
  multiSelect = false,
}: TreeViewProps) {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());

  const handleSelect = (node: TreeNode) => {
    if (multiSelect) {
      const newSelected = new Set(selectedIds);
      if (newSelected.has(node.id)) {
        newSelected.delete(node.id);
      } else {
        newSelected.add(node.id);
      }
      setSelectedIds(newSelected);
    } else {
      setSelectedIds(new Set([node.id]));
    }
    onSelect?.(node);
  };

  const handleExpand = (nodeId: string, expanded: boolean) => {
    const newExpanded = new Set(expandedIds);
    if (expanded) {
      newExpanded.add(nodeId);
    } else {
      newExpanded.delete(nodeId);
    }
    setExpandedIds(newExpanded);
    onExpand?.(nodeId, expanded);
  };

  return (
    <div className={cn('overflow-auto', className)}>
      <div className="py-1">
        {data.map((node) => (
          <TreeNodeComponent
            key={node.id}
            node={node}
            level={0}
            onSelect={handleSelect}
            onExpand={handleExpand}
            showIcons={showIcons}
            selectedIds={selectedIds}
            expandedIds={expandedIds}
          />
        ))}
      </div>
    </div>
  );
}

// Utility functions for working with tree data
export const treeUtils = {
  findNode: (data: TreeNode[], nodeId: string): TreeNode | null => {
    for (const node of data) {
      if (node.id === nodeId) return node;
      if (node.children) {
        const found = treeUtils.findNode(node.children, nodeId);
        if (found) return found;
      }
    }
    return null;
  },

  expandAll: (data: TreeNode[]): Set<string> => {
    const expanded = new Set<string>();
    const traverse = (nodes: TreeNode[]) => {
      nodes.forEach(node => {
        if (node.children && node.children.length > 0) {
          expanded.add(node.id);
          traverse(node.children);
        }
      });
    };
    traverse(data);
    return expanded;
  },

  collapseAll: (): Set<string> => {
    return new Set();
  },

  filterNodes: (data: TreeNode[], predicate: (node: TreeNode) => boolean): TreeNode[] => {
    const filter = (nodes: TreeNode[]): TreeNode[] => {
      return nodes.reduce<TreeNode[]>((acc, node) => {
        const filteredChildren = node.children ? filter(node.children) : [];
        
        if (predicate(node) || filteredChildren.length > 0) {
          acc.push({
            ...node,
            children: filteredChildren,
          });
        }
        
        return acc;
      }, []);
    };
    
    return filter(data);
  },

  searchNodes: (data: TreeNode[], searchTerm: string): TreeNode[] => {
    const search = searchTerm.toLowerCase();
    return treeUtils.filterNodes(data, (node) =>
      node.label.toLowerCase().includes(search)
    );
  },

  getNodePath: (data: TreeNode[], nodeId: string): TreeNode[] => {
    const path: TreeNode[] = [];
    
    const findPath = (nodes: TreeNode[], targetId: string, currentPath: TreeNode[]): boolean => {
      for (const node of nodes) {
        const newPath = [...currentPath, node];
        
        if (node.id === targetId) {
          path.push(...newPath);
          return true;
        }
        
        if (node.children && findPath(node.children, targetId, newPath)) {
          return true;
        }
      }
      return false;
    };
    
    findPath(data, nodeId, []);
    return path;
  },

  getExpandedNodeIds: (data: TreeNode[], nodeId: string): string[] => {
    const path = treeUtils.getNodePath(data, nodeId);
    return path.slice(0, -1).map(node => node.id);
  },
};