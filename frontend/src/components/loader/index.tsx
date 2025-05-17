"use client"

export default function SkeletonLoader() {
	return (
		<div className="animate-pulse space-y-4">
			<div className="h-8 bg-white/20 rounded w-3/4 mx-auto"></div>
			<div className="h-4 bg-white/10 rounded w-full"></div>
			<div className="h-4 bg-white/10 rounded w-full"></div>
			<div className="h-4 bg-white/10 rounded w-1/2"></div>
		</div>
	)
}
