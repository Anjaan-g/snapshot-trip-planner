"use client"

export default function SkeletonLoader() {
	return (
		<div className="animate-pulse space-y-4 max-w-4xl mx-auto">
			<div className="h-8 bg-white/40 rounded w-3/4 mx-auto"></div>
			<div className="h-4 bg-white/40 rounded w-full"></div>
			<div className="h-4 bg-white/40 rounded w-full"></div>
			<div className="h-4 bg-white/40 rounded w-1/2"></div>
		</div>
	)
}
