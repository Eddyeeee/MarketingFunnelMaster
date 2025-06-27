import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Play, Clock, Eye } from "lucide-react";

interface VideoPlayerProps {
  title: string;
  description: string;
  duration: string;
  views: string;
  videoId: string;
  onPlay?: () => void;
  size?: 'normal' | 'large';
}

export default function VideoPlayer({ 
  title, 
  description, 
  duration, 
  views, 
  videoId, 
  onPlay,
  size = 'normal'
}: VideoPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);

  const handlePlay = () => {
    setIsPlaying(true);
    onPlay?.();
    
    // In a real implementation, you would integrate with a video player library
    // For now, we'll show a placeholder
    alert(`${title} Video wird geladen...`);
  };

  const aspectRatio = size === 'large' ? 'aspect-video' : 'aspect-video';
  const thumbnailHeight = size === 'large' ? 'h-96' : 'h-48';

  return (
    <div className="space-y-4">
      <div className="mb-4">
        <h3 className="text-xl font-semibold text-q-neutral-dark mb-2">{title}</h3>
        <p className="text-q-neutral-medium">{description}</p>
      </div>
      
      <div className={`bg-gray-900 rounded-lg ${aspectRatio} ${thumbnailHeight} flex items-center justify-center relative overflow-hidden`}>
        {!isPlaying ? (
          <>
            {/* Thumbnail overlay */}
            <div className="absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 opacity-80"></div>
            <Button 
              onClick={handlePlay}
              className="play-btn bg-q-accent hover:bg-q-accent-dark text-white rounded-full w-16 h-16 flex items-center justify-center transition-all transform hover:scale-110 relative z-10"
            >
              <Play className="ml-1" size={24} />
            </Button>
            {/* Video info overlay */}
            <div className="absolute bottom-4 left-4 text-white z-10">
              <div className="text-sm opacity-90">{title}</div>
            </div>
          </>
        ) : (
          <div className="w-full h-full bg-black flex items-center justify-center">
            <div className="text-white text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
              <p>Video wird geladen...</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="flex justify-between items-center text-sm text-q-neutral-medium">
        <div className="flex items-center space-x-1">
          <Clock size={16} />
          <span>{duration}</span>
        </div>
        <div className="flex items-center space-x-1">
          <Eye size={16} />
          <span>{views}</span>
        </div>
      </div>
    </div>
  );
}
